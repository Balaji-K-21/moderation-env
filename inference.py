import os
import requests
from openai import OpenAI

# ── Configuration ────────────────────────────────────────────────────────────
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "https://kolaaahalan-moderation-env.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable not set.")

client = OpenAI(
    api_key=HF_TOKEN,
    base_url="https://api.groq.com/openai/v1"
)

SESSION = requests.Session()

def reset(task_id: str) -> dict:
    response = SESSION.post(f"{ENV_BASE_URL}/reset", json={"task_id": task_id})
    if not response.ok:
        print("RESET STATUS:", response.status_code)
        print("RESET BODY:", response.text)
    response.raise_for_status()
    return response.json()

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
            print("STEP STATUS:", response.status_code)
            print("STEP BODY:", response.text)
            print("STEP PAYLOAD:", payload)

        response.raise_for_status()
        return response.json()

    except Exception as e:
        print("⚠️ STEP ERROR:", str(e))

        # SAFE FALLBACK → prevent crash
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
    response = SESSION.get(f"{ENV_BASE_URL}/state")
    if not response.ok:
        print("STATE STATUS:", response.status_code)
        print("STATE BODY:", response.text)
    response.raise_for_status()
    return response.json()

def ask_agent(observation: dict, actions_taken=None) -> dict:
    if actions_taken is None:
        actions_taken = []

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

    log = observation.get("investigation_log", [])
    remaining = observation.get("remaining_steps", 6)

    if "fetch_reporter_profile" in actions_taken or remaining <= 2:
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

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.0,
    )

    raw = response.choices[0].message.content.strip()
    print(f"  LLM raw output: {raw}")

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

    log_text = " ".join(observation.get("investigation_log", [])).lower()
    if action_type == "decide":
        if "false reports" in log_text or "0 prior violations" in log_text:
            decision = "OVERTURN"
        elif "valid reports" in log_text or "prior violations" in log_text:
            decision = "UPHOLD"
        elif decision == "NONE":
            decision = "OVERTURN"

    return {"action_type": action_type, "decision": decision}

def choose_next_action(observation: dict, actions_taken: list) -> dict:
    log_text = " ".join(observation.get("investigation_log", [])).lower()
    remaining = observation.get("remaining_steps", 0)

    if "inspect_post" not in actions_taken:
        return {"action_type": "inspect_post", "decision": "NONE"}

    non_english_markers = [
        "language: hindi",
        "language: tamil",
        "language: arabic",
        "language: malayalam",
        "language: bengali",
        "language: bahasa",
        "language: bahasa indonesia",
    ]
    needs_translation = any(marker in log_text for marker in non_english_markers)

    if needs_translation and "request_translation" not in actions_taken:
        return {"action_type": "request_translation", "decision": "NONE"}

    if "fetch_user_history" not in actions_taken:
        return {"action_type": "fetch_user_history", "decision": "NONE"}

    if "fetch_reporter_profile" not in actions_taken:
        return {"action_type": "fetch_reporter_profile", "decision": "NONE"}

    ambiguous_signals = [
        "mixed",
        "proceed carefully",
        "0 prior violations",
        "false reports",
    ]
    if any(signal in log_text for signal in ambiguous_signals):
        if "fetch_similar_rulings" not in actions_taken and remaining > 1:
            return {"action_type": "fetch_similar_rulings", "decision": "NONE"}

    return ask_agent(observation, actions_taken)

def run_episode(task_id: str) -> float:
    print(f"\n{'=' * 50}")
    print(f"Task: {task_id.upper()}")
    print(f"{'=' * 50}")

    response = reset(task_id)

    if "observation" in response and isinstance(response["observation"], dict):
        observation = response["observation"]
        if "reward" in response and "reward" not in observation:
            observation["reward"] = response["reward"]
        if "done" in response and "done" not in observation:
            observation["done"] = response["done"]
    else:
        observation = response

    print(f"  Case selected : {observation.get('post_content', '')}")

    total_reward = 0.0
    step_count = 0
    actions_taken = []

    while not observation.get("done", False) and observation.get("remaining_steps", 0) > 0:
        action = choose_next_action(observation, actions_taken)
        actions_taken.append(action["action_type"])

        print(f"\nStep {step_count + 1}")
        print(f"  Chosen action : {action['action_type']}")
        if action["action_type"] == "decide":
            print(f"  Decision      : {action['decision']}")

        result = step(action["action_type"], action["decision"])

        if "observation" in result and isinstance(result["observation"], dict):
            observation = result["observation"]
            if "reward" in result and "reward" not in observation:
                observation["reward"] = result["reward"]
            if "done" in result and "done" not in observation:
                observation["done"] = result["done"]
        else:
            observation = result

        reward = observation.get("reward", result.get("reward", 0.0))
        total_reward += reward
        step_count += 1

        print(f"  Reward        : {reward:.2f}")
        print(f"  Remaining     : {observation.get('remaining_steps', 0)}")
        print(f"  Log           : {observation.get('investigation_log', [])}")

        if action["action_type"] == "decide" or observation.get("done", False):
            break

    print(f"\nFinal reward for {task_id}: {total_reward:.2f}")
    return total_reward

if __name__ == "__main__":
    tasks = ["easy_appeal", "medium_appeal", "hard_appeal"]
    scores = {}

    for task in tasks:
        SESSION.cookies.clear()
        scores[task] = run_episode(task)

    print(f"\n{'=' * 50}")
    print("FINAL SCORES")
    print(f"{'=' * 50}")
    for task, score in scores.items():
        print(f"  {task}: {score:.2f}")

    total = sum(scores.values())
    print(f"\n  Total score: {total:.2f}")