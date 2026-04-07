import os
import sys
import requests
from openai import OpenAI

# ── Configuration ────────────────────────────────────────────────────────────
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "https://kolaaahalan-moderation-env.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

# Scaler / evaluator-provided proxy credentials
EVAL_API_BASE_URL = os.getenv("API_BASE_URL")
EVAL_API_KEY = os.getenv("API_KEY")

# Local fallback credentials
HF_TOKEN = os.getenv("HF_TOKEN")
LOCAL_BASE_URL = "https://api.groq.com/openai/v1"

client = None

# Prefer evaluator-provided proxy
if EVAL_API_KEY and EVAL_API_BASE_URL:
    client = OpenAI(
        api_key=EVAL_API_KEY,
        base_url=EVAL_API_BASE_URL,
    )
# Fallback to local Groq setup
elif HF_TOKEN:
    client = OpenAI(
        api_key=HF_TOKEN,
        base_url=LOCAL_BASE_URL,
    )

SESSION = requests.Session()


def emit(line: str) -> None:
    print(line, flush=True)


def warn(line: str) -> None:
    print(line, file=sys.stderr, flush=True)


def reset(task_id: str) -> dict:
    try:
        response = SESSION.post(
            f"{ENV_BASE_URL}/reset",
            json={"task_id": task_id},
            timeout=30,
        )
        if not response.ok:
            warn(f"RESET STATUS: {response.status_code}")
            warn(f"RESET BODY: {response.text}")
        response.raise_for_status()
        return response.json()

    except Exception as e:
        warn(f"⚠️ RESET ERROR: {str(e)}")
        return {
            "observation": {
                "post_content": "",
                "appeal_text": "",
                "available_actions": [],
                "investigation_log": ["Reset failed - fallback triggered"],
                "remaining_steps": 0,
                "reward": -1.0,
                "done": True,
            },
            "reward": -1.0,
            "done": True,
        }


def step(action_type: str, decision: str = "NONE") -> dict:
    payload = {
        "action": {
            "action_type": action_type,
            "decision": decision if action_type == "decide" else None,
        }
    }

    try:
        response = SESSION.post(
            f"{ENV_BASE_URL}/step",
            json=payload,
            timeout=30,
        )

        if not response.ok:
            warn(f"STEP STATUS: {response.status_code}")
            warn(f"STEP BODY: {response.text}")
            warn(f"STEP PAYLOAD: {payload}")

        response.raise_for_status()
        return response.json()

    except Exception as e:
        warn(f"⚠️ STEP ERROR: {str(e)}")

        return {
            "observation": {
                "post_content": "",
                "appeal_text": "",
                "available_actions": [],
                "investigation_log": ["Step failed - fallback triggered"],
                "remaining_steps": 0,
                "reward": -1.0,
                "done": True,
            },
            "reward": -1.0,
            "done": True,
        }


def get_state() -> dict:
    try:
        response = SESSION.get(f"{ENV_BASE_URL}/state", timeout=30)
        if not response.ok:
            warn(f"STATE STATUS: {response.status_code}")
            warn(f"STATE BODY: {response.text}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        warn(f"⚠️ STATE ERROR: {str(e)}")
        return {}


def ask_agent(observation: dict, actions_taken=None) -> dict:
    if actions_taken is None:
        actions_taken = []

    log = observation.get("investigation_log", [])
    remaining = observation.get("remaining_steps", 6)
    log_text = " ".join(log).lower()

    evidence_count = len(set(actions_taken) & {
        "inspect_post",
        "fetch_user_history",
        "fetch_reporter_profile",
        "fetch_similar_rulings",
        "request_translation"
    })

    def fallback_policy() -> dict:
        needs_translation = (
            "language:" in log_text
            and "language: english" not in log_text
            and "request_translation" not in actions_taken
        )

        if needs_translation:
            return {"action_type": "request_translation", "decision": "NONE"}

        if evidence_count < 2:
            for candidate in [
                "fetch_user_history",
                "fetch_reporter_profile",
                "fetch_similar_rulings",
            ]:
                if candidate not in actions_taken:
                    return {"action_type": candidate, "decision": "NONE"}

        if "false reports" in log_text or "0 prior violations" in log_text:
            return {"action_type": "decide", "decision": "OVERTURN"}
        elif "valid reports" in log_text or "prior violations" in log_text:
            return {"action_type": "decide", "decision": "UPHOLD"}
        else:
            return {"action_type": "decide", "decision": "OVERTURN"}

    if client is None:
        warn("⚠️ No LLM client available, using fallback policy.")
        return fallback_policy()

    system_prompt = """You are a content moderation appeal investigator.
You will be given a flagged post and a user's appeal.
Your job is to investigate the case and decide whether to UPHOLD or OVERTURN the removal.

You have these actions available:
- inspect_post: See full post details
- fetch_user_history: Check the user's past violations
- fetch_reporter_profile: Check the reporter's credibility
- fetch_similar_rulings: See how similar cases were ruled
- request_translation: Translate non-English content
- decide: Make your final ruling (requires decision: UPHOLD or OVERTURN)

Respond in this exact format:
ACTION: <action_type>
DECISION: <UPHOLD or OVERTURN or NONE>

Only use UPHOLD or OVERTURN when ACTION is decide. Use NONE otherwise.
Be efficient — you have a limited number of steps."""

    if evidence_count >= 3 or remaining <= 2:
        force_decide = "\nIMPORTANT: You MUST now call decide with UPHOLD or OVERTURN. No more investigation."
    else:
        force_decide = ""

    user_prompt = f"""
Post: {observation.get('post_content')}
Appeal: {observation.get('appeal_text')}
Steps remaining: {remaining}
Actions already taken: {', '.join(actions_taken) or 'None'}
Investigation log:
{chr(10).join(log) or 'Nothing gathered yet.'}
{force_decide}

What is your next action?
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
        )

        raw = response.choices[0].message.content.strip()
        warn(f"LLM raw output: {raw}")

        action_type = "decide"
        decision = "NONE"
        raw_lower = raw.lower()

        if "overturn" in raw_lower:
            action_type = "decide"
            decision = "OVERTURN"
        elif "uphold" in raw_lower:
            action_type = "decide"
            decision = "UPHOLD"
        else:
            valid_actions = [
                "inspect_post",
                "fetch_user_history",
                "fetch_reporter_profile",
                "fetch_similar_rulings",
                "request_translation",
            ]
            for line in raw.splitlines():
                line_lower = line.strip().lower()
                for valid_action in valid_actions:
                    if valid_action in line_lower:
                        action_type = valid_action
                        decision = "NONE"
                        break
                if action_type != "decide" or decision != "NONE":
                    break

        if action_type == "decide":
            if "false reports" in log_text or "0 prior violations" in log_text:
                decision = "OVERTURN"
            elif "valid reports" in log_text or "prior violations" in log_text:
                decision = "UPHOLD"
            elif decision == "NONE":
                decision = "OVERTURN"

        return {"action_type": action_type, "decision": decision}

    except Exception as e:
        warn(f"⚠️ LLM ERROR: {str(e)}")
        return fallback_policy()


def choose_next_action(observation: dict, actions_taken: list) -> dict:
    if "inspect_post" not in actions_taken:
        return {"action_type": "inspect_post", "decision": "NONE"}

    investigation_actions = {
        "inspect_post",
        "fetch_user_history",
        "fetch_reporter_profile",
        "fetch_similar_rulings",
        "request_translation",
    }

    log_text = " ".join(observation.get("investigation_log", [])).lower()

    needs_translation = (
        "language:" in log_text
        and "language: english" not in log_text
        and "request_translation" not in actions_taken
    )
    if needs_translation:
        return {"action_type": "request_translation", "decision": "NONE"}

    if len(set(actions_taken) & investigation_actions) < 2:
        for candidate in [
            "fetch_user_history",
            "fetch_reporter_profile",
            "fetch_similar_rulings",
        ]:
            if candidate not in actions_taken:
                return {"action_type": candidate, "decision": "NONE"}

    action = ask_agent(observation, actions_taken)

    if action["action_type"] in actions_taken and action["action_type"] != "decide":
        for candidate in [
            "request_translation",
            "fetch_user_history",
            "fetch_reporter_profile",
            "fetch_similar_rulings",
        ]:
            if candidate == "request_translation" and not needs_translation:
                continue
            if candidate not in actions_taken:
                return {"action_type": candidate, "decision": "NONE"}

        return {"action_type": "decide", "decision": "OVERTURN"}

    if action["action_type"] == "decide" and len(set(actions_taken) & investigation_actions) < 3:
        for candidate in [
            "fetch_user_history",
            "fetch_reporter_profile",
            "fetch_similar_rulings",
        ]:
            if candidate not in actions_taken:
                return {"action_type": candidate, "decision": "NONE"}

    return action


def run_episode(task_id: str) -> float:
    emit(f"[START] task={task_id}")

    response = reset(task_id)

    if "observation" in response and isinstance(response["observation"], dict):
        observation = response["observation"]
        if "reward" in response and "reward" not in observation:
            observation["reward"] = response["reward"]
        if "done" in response and "done" not in observation:
            observation["done"] = response["done"]
    else:
        observation = response

    total_reward = 0.0
    step_count = 0
    actions_taken = []

    while not observation.get("done", False) and observation.get("remaining_steps", 0) > 0:
        action = choose_next_action(observation, actions_taken)
        actions_taken.append(action["action_type"])

        result = step(action["action_type"], action["decision"])

        if "observation" in result and isinstance(result["observation"], dict):
            observation = result["observation"]
            if "reward" in result and "reward" not in observation:
                observation["reward"] = result["reward"]
            if "done" in result and "done" not in observation:
                observation["done"] = result["done"]
        else:
            observation = result

        reward = float(observation.get("reward", result.get("reward", 0.0)))
        total_reward += reward
        step_count += 1

        emit(
            f"[STEP] task={task_id} "
            f"step={step_count} "
            f"action={action['action_type']} "
            f"decision={action['decision']} "
            f"reward={reward:.2f} "
            f"remaining={observation.get('remaining_steps', 0)} "
            f"done={observation.get('done', False)}"
        )

        if action["action_type"] == "decide" or observation.get("done", False):
            break

    emit(f"[END] task={task_id} score={total_reward:.2f} steps={step_count}")
    return total_reward


if __name__ == "__main__":
    tasks = ["easy_appeal", "medium_appeal", "hard_appeal"]
    scores = {}

    for task in tasks:
        SESSION.cookies.clear()
        scores[task] = run_episode(task)

    total = sum(scores.values())
    emit(f"[END] task=overall score={total:.2f} steps={len(tasks)}")