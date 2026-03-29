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
| Correct decision (easy) | +1.0 |
| Correct decision (medium) | +1.2 |
| Correct decision (hard) | +1.5 |
| Translation bonus | +0.2 to +0.3 |
| Step cost | -0.05 to -0.15 |
| False positive | -1.5 to -2.0 |
| False negative | -1.0 to -1.5 |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | /reset | Start a new episode |
| POST | /step | Submit an action |
| GET | /state | Get current state |
| GET | /health | Health check |

## Setup

### Install dependencies
```bash
pip install -r requirements.txt
```

### Set environment variables
```bash
export HF_TOKEN=your_groq_api_key
export ENV_BASE_URL=http://localhost:8000
```

### Run server
```bash
uvicorn server.app:app --host 0.0.0.0 --port 8000 --reload
```

### Run inference
```bash
python inference.py
```

## Example Episode
```
reset(task_id="easy_appeal")
→ Post: "BUY CHEAP PHARMA NOW! LINK IN BIO!!!"
→ Appeal: "This is not spam, I am just sharing a deal."

step(inspect_post)            → reward: -0.05
step(fetch_user_history)      → reward: -0.05
step(fetch_reporter_profile)  → reward: -0.05
step(decide, UPHOLD)          → reward: +0.95
Total reward: 0.80
```

## Environment Variables

| Variable | Description |
|---|---|
| ENV_BASE_URL | The API endpoint for the environment |
| MODEL_NAME | LLM model identifier |
| HF_TOKEN | Groq API key for LLM inference |

## Live Demo

[https://kolaaahalan-moderation-env.hf.space](https://kolaaahalan-moderation-env.hf.space)