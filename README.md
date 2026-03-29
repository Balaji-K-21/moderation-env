---
title: Moderation Env
emoji: ⚡
colorFrom: blue
colorTo: gray
sdk: docker
pinned: false
license: mit
---

# Content Moderation Appeal Investigator

An open reinforcement learning environment for training AI agents to investigate
content moderation appeals using multi-step evidence gathering.

## The Problem

Meta's AI moderation systems make single-pass decisions — flag, remove, done.
There is no investigative reasoning layer. The 2025 Instagram ban wave affected
millions of users because innocent content was removed with no second-pass review.
This environment trains agents to investigate before deciding.

## What the Agent Does

The agent receives a flagged post and a user's appeal. It has a budget of actions
to gather evidence before making a final ruling: UPHOLD (keep the removal) or
OVERTURN (restore the content).

## Tasks

| Task | Difficulty | Description |
|---|---|---|
| easy_appeal | Easy | Clear spam with obvious signals |
| medium_appeal | Medium | Ambiguous frustration language |
| hard_appeal | Hard | Non-English political speech |

## Action Space

| Action | Description |
|---|---|
| inspect_post | See full post content and metadata |
| fetch_user_history | Check user's past violations |
| fetch_reporter_profile | Check reporter credibility |
| fetch_similar_rulings | See precedent cases |
| request_translation | Translate non-English content |
| decide | Final ruling — UPHOLD or OVERTURN |

## Reward Function

| Event | Reward |
|---|---|
| Correct decision | +1.0 |
| Translation bonus (non-English) | +0.2 |
| Step cost (per action) | -0.1 |
| False negative (missed violation) | -1.0 |
| False positive (banned innocent) | -1.5 |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /reset | Start a new episode |
| POST | /step | Submit an action |
| GET | /state | Get current state |
| GET | /health | Health check |

## Setup
```bash
git clone https://huggingface.co/spaces/kolaaahalan/moderation-env
cd moderation-env
pip install -r requirements.txt
uvicorn server.app:app --host 0.0.0.0 --port 8000
```

## Run Baseline Agent
```bash
export GROQ_API_KEY=your-key-here
python inference.py
```

## Example Episode
```
reset(task_id="easy_appeal")
→ Post: "BUY CHEAP PHARMA NOW! LINK IN BIO!!!"
→ Appeal: "This is not spam, I am just sharing a deal."

step(inspect_post)     → reward: -0.1
step(decide, UPHOLD)   → reward: +0.9
Total reward: 0.80
```

## Environment Variables

| Variable | Description |
|---|---|
| API_BASE_URL | The API endpoint for the environment |
| MODEL_NAME | LLM model identifier |
| HF_TOKEN | Hugging Face API token |

## Live Demo

[https://kolaaahalan-moderation-env.hf.space](https://kolaaahalan-moderation-env.hf.space)