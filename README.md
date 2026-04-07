# 🛡️ Moderation Appeal Investigator

An AI-powered decision-making system that investigates content moderation appeals using structured reasoning and reinforcement-style interaction.

---

## 🚀 Overview

Most moderation systems act like **black boxes** — they classify content instantly with little transparency.

This project introduces a different approach:

> Instead of guessing, the system **investigates before deciding**.

The agent:
- Gathers evidence step-by-step  
- Evaluates multiple signals  
- Makes a final decision with reasoning  

---

## 🧠 How It Works

The system is designed as an **interactive environment**, where an AI agent performs actions to investigate a case.

### 🔍 Available Actions
- `inspect_post` → Understand the content  
- `fetch_user_history` → Check prior violations  
- `fetch_reporter_profile` → Evaluate reporter credibility  
- `fetch_similar_rulings` → Look at precedents  
- `request_translation` → Handle non-English content  
- `decide` → Final decision (UPHOLD / OVERTURN)

---

## ⚙️ Decision Strategy

The agent follows a structured reasoning flow:

1. Always inspect the content  
2. Gather multiple signals (user, reporter, precedents)  
3. Handle multilingual cases via translation  
4. Only decide after sufficient evidence  

This ensures:
- No premature decisions  
- Consistent reasoning  
- Efficient use of limited steps  

---

## 🎯 Key Features

### ✅ Evidence-Based Moderation
Decisions are based on multiple signals, not just text classification.

### 🌍 Multilingual Understanding
Handles non-English posts through translation before reasoning.

### 🧩 Step-Constrained Reasoning
Agent must make decisions within limited steps — mimicking real-world constraints.

### 🔁 Reinforcement Learning Setup
Environment provides rewards for:
- Correct decisions  
- Efficient investigation  
- Avoiding false positives/negatives  

---

## 📊 Example Flow

**Simple case:**
inspect_post → fetch_user_history → fetch_reporter_profile → decide

**Complex case:**
inspect_post → request_translation → fetch_user_history → fetch_similar_rulings → decide

---

## 🏗️ Architecture

- **Environment:** OpenEnv-based simulation  
- **Agent:** LLM-driven decision policy  
- **Backend:** FastAPI environment server  
- **Inference:** Iterative action selection loop  

---

## 📈 Results

| Task | Score |
|------|------|
| Easy | 0.80 |
| Medium | 0.80 |
| Hard | 1.20 |
| **Total** | **2.80** |

---

## 🧠 Why This Matters

Content moderation is not just about classification — it's about **context, intent, and evidence**.

This system demonstrates how AI can:
- Reason step-by-step  
- Reduce wrongful moderation decisions  
- Improve transparency in decision-making  

---

## 🔮 Future Improvements

- Learning-based policy instead of rule-guided logic  
- Memory across multiple cases  
- Human-in-the-loop feedback integration  
- Explainable decision reports  

---

## 🏁 Conclusion

This project moves moderation from:

❌ Instant classification  
→  
✅ Structured investigation and reasoning  

---

## 👤 Author

Balaji K