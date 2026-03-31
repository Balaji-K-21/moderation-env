---

title: Moderation Env
emoji: ⚡
colorFrom: blue
colorTo: gray
sdk: docker
pinned: false
license: mit
------------

# Content Moderation Appeal Investigator

A reinforcement learning environment where agents must **investigate before deciding**.

Unlike traditional moderation systems that make single-pass classification decisions, this environment requires agents to gather evidence across multiple steps under uncertainty.

The goal is not just to classify content — but to simulate **real-world moderation reasoning**.

---

## The Problem

Modern AI moderation systems operate as classifiers: input → decision → done.

However, real-world moderation requires:

* evaluating context
* checking user history
* assessing reporter credibility
* interpreting ambiguous or multilingual content

Failures in these systems (e.g., large-scale wrongful bans) highlight the absence of an **investigation layer**.

This environment introduces that missing layer.

---

## Key Design Principles

### 🔍 Investigation over classification

Agents must take multiple actions to gather evidence before making a decision.

### 🎲 Controlled randomness with reproducibility

Each task samples from a pool of cases:

* deterministic when `seed` or `episode_id` is provided
* deterministic rotation fallback otherwise

This ensures:

* diverse evaluation
* reproducible benchmarking

### ⚖️ Noisy and non-deterministic evidence

Evidence is intentionally imperfect:

* trusted reporters can be wrong
* suspicious users can be correct
* precedent cases can be mixed

Agents must reason under uncertainty — not rely on shortcuts.

### 🌍 Real-world ambiguity

Tasks include:

* sarcasm and idiomatic language
* political speech vs incitement
* misinformation vs personal experience
* multilingual content with translation uncertainty

---

## What the Agent Does

The agent receives a flagged post and a user's appeal. It has a budget of actions
to gather evidence before making a final ruling:

* **UPHOLD** → keep the removal
* **OVERTURN** → restore the content

---

## Tasks

Each task represents a difficulty tier.
Cases are **sampled from a pool**, not fixed.

| Task          | Difficulty | Description                                   |
| ------------- | ---------- | --------------------------------------------- |
| easy_appeal   | Easy       | Clear signals (spam, scams, benign posts)     |
| medium_appeal | Medium     | Ambiguous intent, subjective interpretation   |
| hard_appeal   | Hard       | Multilingual, policy edge cases, nuanced harm |

---

## Action Space

| Action                 | Description                        |
| ---------------------- | ---------------------------------- |
| inspect_post           | See full post content and metadata |
| fetch_user_history     | Check user's past violations       |
| fetch_reporter_profile | Check reporter credibility         |
| fetch_similar_rulings  | See precedent cases                |
| request_translation    | Translate non-English content      |
| decide                 | Final ruling — UPHOLD or OVERTURN  |

---

## Reward Function

Rewards encourage:

* efficient investigation
* correct decisions
* avoiding premature conclusions

| Event                      | Reward         |
| -------------------------- | -------------- |
| Correct decision (easy)    | +1.0           |
| Correct decision (medium)  | +1.2           |
| Correct decision (hard)    | +1.5           |
| Translation bonus          | +0.1 to +0.15  |
| Step cost                  | -0.05 to -0.15 |
| False positive             | -1.5 to -2.0   |
| False negative             | -1.0 to -1.5   |
| Premature decision penalty | -0.25          |

---

## API Endpoints

| Method | Endpoint | Description         |
| ------ | -------- | ------------------- |
| POST   | /reset   | Start a new episode |
| POST   | /step    | Submit an action    |
| GET    | /state   | Get current state   |
| GET    | /health  | Health check        |

---

## Setup

### Install dependencies

```bash
pip install -r requirements.txt
```

### Set environment variables

```bash
export HF_TOKEN=your_huggingface_token
export MODEL_NAME=your_model_name
export API_BASE_URL=https://router.huggingface.co/v1
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

---

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

---

## Environment Variables

| Variable     | Description                             |
| ------------ | --------------------------------------- |
| ENV_BASE_URL | API endpoint for the environment        |
| MODEL_NAME   | LLM model identifier                    |
| API_BASE_URL | OpenAI-compatible model endpoint        |
| HF_TOKEN     | Hugging Face API token for model access |

---

## Live Demo

https://kolaaahalan-moderation-env.hf.space

---

This environment bridges the gap between classification and reasoning —
training agents to act like investigators, not just predictors.
