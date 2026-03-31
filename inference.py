import os
import re
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME")
HF_TOKEN = os.getenv("HF_TOKEN")
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "https://kolaaahalan-moderation-env.hf.space")

if not MODEL_NAME:
    raise ValueError("MODEL_NAME environment variable not set.")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN environment variable not set.")

client = OpenAI(
    api_key=HF_TOKEN,
    base_url=API_BASE_URL,
)

SESSION = requests.Session()

ACTION_RE = re.compile(r"ACTION:\s*(\w+)", re.IGNORECASE)
DECISION_RE = re.compile(r"DECISION:\s*(UPHOLD|OVERTURN|NONE)", re.IGNORECASE)

VALID_ACTIONS = {
    "inspect_post",
    "fetch_user_history",
    "fetch_reporter_profile",
    "fetch_similar_rulings",
    "request_translation",
    "decide",
}


def reset(task_id: str, seed: int = 42) -> dict:
    response = SESSION.post(
        f"{ENV_BASE_URL}/reset",
        json={"task_id": task_id, "seed": seed},
        timeout=30
    )
    if not response.ok:
        print("RESET STATUS:", response.status_code)
        print("RESET BODY:", response.text)
    response.raise_for_status()
    return response.json()


def step(action_type: str, decision: str = "NONE") -> dict:
    payload = {
        "action": {
            "action_type": action_type,
            "decision": decision if action_type == "decide" else None
        }
    }
    response = SESSION.post(f"{ENV_BASE_URL}/step", json=payload,
        timeout=30
    )
    if not response.ok:
        print("STEP STATUS:", response.status_code)
        print("STEP BODY:", response.text)
    response.raise_for_status()
    return response.json()


def get_observation(response_json: dict) -> dict:
    if "observation" in response_json and isinstance(response_json["observation"], dict):
        observation = response_json["observation"]
        if "reward" in response_json and "reward" not in observation:
            observation["reward"] = response_json["reward"]
        if "done" in response_json and "done" not in observation:
            observation["done"] = response_json["done"]
        return observation
    return response_json


def ask_agent(observation: dict, actions_taken=None) -> dict:
    if actions_taken is None:
        actions_taken = []

    system_prompt = """You are a content moderation appeal investigator.

Decide the next best action for investigating a moderation appeal.

Return exactly in this format:
ACTION: <action_type>
DECISION: <UPHOLD or OVERTURN or NONE>

Valid actions:
- inspect_post
- fetch_user_history
- fetch_reporter_profile
- fetch_similar_rulings
- request_translation
- decide

Rules:
- Use DECISION: NONE for every action except decide.
- Only use UPHOLD or OVERTURN when ACTION is decide.
- Avoid repeating actions already taken unless you are deciding.
- Investigate efficiently because steps are limited.
"""

    user_prompt = f"""
Post: {observation.get('post_content')}
Appeal: {observation.get('appeal_text')}
Steps remaining: {observation.get('remaining_steps', 0)}
Available actions: {', '.join(observation.get('available_actions', []))}
Actions already taken: {', '.join(actions_taken) or 'None'}

Investigation log:
{chr(10).join(observation.get('investigation_log', [])) or 'Nothing gathered yet.'}
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

    action_match = ACTION_RE.search(raw)
    decision_match = DECISION_RE.search(raw)

    action_type = action_match.group(1) if action_match else "decide"
    decision = decision_match.group(1).upper() if decision_match else "OVERTURN"

    if action_type not in VALID_ACTIONS:
        action_type = "decide"
        decision = "OVERTURN"

    if action_type != "decide":
        decision = "NONE"

    return {"action_type": action_type, "decision": decision}


def choose_next_action(observation: dict, actions_taken: list) -> dict:
    if "inspect_post" not in actions_taken:
        return {"action_type": "inspect_post", "decision": "NONE"}

    action = ask_agent(observation, actions_taken)

    if action["action_type"] in actions_taken and action["action_type"] != "decide":
        log_text = " ".join(observation.get("investigation_log", [])).lower()

        fallback_order = []
        if "language:" in log_text and "language: english" not in log_text and "request_translation" not in actions_taken:
            fallback_order.append("request_translation")

        fallback_order.extend([
            "fetch_user_history",
            "fetch_reporter_profile",
            "fetch_similar_rulings",
        ])

        for candidate in fallback_order:
            if candidate not in actions_taken:
                return {"action_type": candidate, "decision": "NONE"}

        return {"action_type": "decide", "decision": "OVERTURN"}

    return action


def run_episode(task_id: str, seed: int = 42) -> float:
    print(f"\n{'=' * 50}")
    print(f"Task: {task_id.upper()}")
    print(f"{'=' * 50}")

    response = reset(task_id, seed=seed)
    observation = get_observation(response)

    print(f"  Initial post preview: {observation.get('post_content', '')}")

    total_reward = 0.0
    step_count = 0
    actions_taken = []

    while not observation.get("done", False) and observation.get("remaining_steps", 0) > 0:
        action = choose_next_action(observation, actions_taken)

        if action["action_type"] != "decide" and action["action_type"] in actions_taken:
            action = {"action_type": "decide", "decision": "OVERTURN"}

        actions_taken.append(action["action_type"])

        print(f"\nStep {step_count + 1}")
        print(f"  Chosen action : {action['action_type']}")
        if action["action_type"] == "decide":
            print(f"  Decision      : {action['decision']}")

        result = step(action["action_type"], action["decision"])
        observation = get_observation(result)

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

    for idx, task in enumerate(tasks):
        SESSION.cookies.clear()
        scores[task] = run_episode(task, seed=42 + idx)

    print(f"\n{'=' * 50}")
    print("FINAL SCORES")
    print(f"{'=' * 50}")
    for task, score in scores.items():
        print(f"  {task}: {score:.2f}")

    total = sum(scores.values())
    print(f"\n  Total score: {total:.2f}")