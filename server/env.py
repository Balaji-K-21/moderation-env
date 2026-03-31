from typing import Optional
import random

from openenv.core.env_server import Environment
from models import ModerationObservation, ModerationAction, ModerationState


class ModerationEnv(Environment[ModerationAction, ModerationObservation, ModerationState]):
    def __init__(self):
        super().__init__()

        self.cases = {
            # ── EASY CASES ─────────────────────────────────────────────────
            "easy_001": {
                "post": "BUY CHEAP PHARMA NOW! LINK IN BIO!!!",
                "appeal": "This is not spam, I am just sharing a deal.",
                "violation": True,
                "lang": "English",
                "difficulty": "easy",
                "reporter_trust": 0.82,
                "user_history_summary": "User history: Account age 14 days, 1 prior spam warning, phone unverified.",
                "reporter_profile_summary": "Reporter trust score: 0.82. Reporter usually files valid reports, but not perfectly.",
                "similar_rulings_summary": "Similar rulings: 2 of 3 precedent cases were UPHOLD. Posts promoting unverified pharma deals are often removed.",
            },
            "easy_002": {
                "post": "MAKE $5000 A DAY FROM HOME! NO EXPERIENCE NEEDED! CLICK HERE!!!",
                "appeal": "I am just sharing a business opportunity.",
                "violation": True,
                "lang": "English",
                "difficulty": "easy",
                "reporter_trust": 0.80,
                "user_history_summary": "User history: Account age 45 days, no verified identity, prior warning for deceptive promotion.",
                "reporter_profile_summary": "Reporter trust score: 0.80. Strong record of accurate spam reports.",
                "similar_rulings_summary": "Similar rulings: 3 of 3 comparable deceptive earnings claims were UPHOLD.",
            },
            "easy_003": {
                "post": "FREE iPhone 15 giveaway! Just send $50 processing fee to claim yours!",
                "appeal": "This is a legitimate giveaway promotion.",
                "violation": True,
                "lang": "English",
                "difficulty": "easy",
                "reporter_trust": 0.77,
                "user_history_summary": "User history: Account age 120 days, one prior complaint related to misleading promotions.",
                "reporter_profile_summary": "Reporter trust score: 0.77. Mostly reliable, with occasional over-reporting.",
                "similar_rulings_summary": "Similar rulings: 3 of 3 cases involving fees for prize claims were UPHOLD.",
            },
            "easy_004": {
                "post": "Just finished my morning run! 5km in 28 minutes, new personal best!",
                "appeal": "I was just sharing my fitness progress, this is not spam.",
                "violation": False,
                "lang": "English",
                "difficulty": "easy",
                "reporter_trust": 0.22,
                "user_history_summary": "User history: Account age 980 days, no prior violations, verified profile.",
                "reporter_profile_summary": "Reporter trust score: 0.22. History includes several false or low-quality reports.",
                "similar_rulings_summary": "Similar rulings: 3 of 3 benign personal fitness updates were OVERTURN.",
            },
            "easy_005": {
                "post": "Happy birthday to my amazing mom! Love you to the moon and back 🎂❤️",
                "appeal": "This is a personal birthday message, not a violation.",
                "violation": False,
                "lang": "English",
                "difficulty": "easy",
                "reporter_trust": 0.12,
                "user_history_summary": "User history: Account age 1500 days, no prior violations, verified account.",
                "reporter_profile_summary": "Reporter trust score: 0.12. Repeated history of mistaken reports.",
                "similar_rulings_summary": "Similar rulings: 3 of 3 personal celebratory messages were OVERTURN.",
            },
            "easy_006": {
                "post": "URGENT: Your account has been compromised! Click this link NOW to secure it: bit.ly/fake123",
                "appeal": "I was trying to help people secure their accounts.",
                "violation": True,
                "lang": "English",
                "difficulty": "easy",
                "reporter_trust": 0.90,
                "user_history_summary": "User history: Account age 7 days, unverified contact details, previous phishing-related removal.",
                "reporter_profile_summary": "Reporter trust score: 0.90. Strong history of valid safety reports.",
                "similar_rulings_summary": "Similar rulings: 3 of 3 credential-theft style warnings with suspicious links were UPHOLD.",
            },
            "easy_007": {
                "post": "Lost my dog near Central Park today. Brown labrador, answers to Max. Please share!",
                "appeal": "I was just trying to find my lost pet, not violating any rules.",
                "violation": False,
                "lang": "English",
                "difficulty": "easy",
                "reporter_trust": 0.18,
                "user_history_summary": "User history: Account age 620 days, no prior violations.",
                "reporter_profile_summary": "Reporter trust score: 0.18. Reporter often flags harmless local posts as spam.",
                "similar_rulings_summary": "Similar rulings: 2 of 3 community help requests were OVERTURN.",
            },
            "easy_008": {
                "post": "Get rich quick with crypto! 1000% returns guaranteed! DM me NOW before it's too late!!!",
                "appeal": "Cryptocurrency investment is legal and I was sharing opportunities.",
                "violation": True,
                "lang": "English",
                "difficulty": "easy",
                "reporter_trust": 0.79,
                "user_history_summary": "User history: Account age 60 days, one prior removal for misleading financial claims.",
                "reporter_profile_summary": "Reporter trust score: 0.79. Reporter usually flags investment scams correctly.",
                "similar_rulings_summary": "Similar rulings: 3 of 3 guaranteed-return promotions were UPHOLD.",
            },
            "easy_009": {
                "post": "Beautiful sunset at the beach today 🌅 Nature is amazing!",
                "appeal": "This is just a photo of a sunset, completely harmless.",
                "violation": False,
                "lang": "English",
                "difficulty": "easy",
                "reporter_trust": 0.20,
                "user_history_summary": "User history: Account age 400 days, no prior violations.",
                "reporter_profile_summary": "Reporter trust score: 0.20. History includes frequent mistaken reports.",
                "similar_rulings_summary": "Similar rulings: 3 of 3 scenic photo posts were OVERTURN.",
            },
            "easy_010": {
                "post": "Buy followers cheap! 10000 followers for $5! Real accounts guaranteed!",
                "appeal": "This is a marketing service, not against any rules.",
                "violation": True,
                "lang": "English",
                "difficulty": "easy",
                "reporter_trust": 0.84,
                "user_history_summary": "User history: Account age 30 days, 2 prior platform-manipulation warnings.",
                "reporter_profile_summary": "Reporter trust score: 0.84. Good history in manipulation-related reports.",
                "similar_rulings_summary": "Similar rulings: 3 of 3 follower-selling services were UPHOLD.",
            },

            # ── MEDIUM CASES ───────────────────────────────────────────────
            "medium_001": {
                "post": "I hate how everyone in this group acts like a child.",
                "appeal": "I was expressing frustration, not harassing anyone.",
                "violation": False,
                "lang": "English",
                "difficulty": "medium",
                "reporter_trust": 0.42,
                "user_history_summary": "User history: Account age 900 days, one prior warning for heated language, no harassment removals.",
                "reporter_profile_summary": "Reporter trust score: 0.42. Mixed history — some valid interpersonal safety reports, some false alarms.",
                "similar_rulings_summary": "Similar rulings: Mixed. Broad insults without a protected target are often allowed but monitored.",
            },
            "medium_002": {
                "post": "These politicians are destroying our country. They should all be thrown out.",
                "appeal": "This is political opinion, protected free speech.",
                "violation": False,
                "lang": "English",
                "difficulty": "medium",
                "reporter_trust": 0.48,
                "user_history_summary": "User history: Account age 1300 days, no prior violent-threat removals.",
                "reporter_profile_summary": "Reporter trust score: 0.48. Reporter history is mixed.",
                "similar_rulings_summary": "Similar rulings: Mostly allowed when framed as political criticism rather than explicit violence.",
            },
            "medium_003": {
                "post": "I want to kill this presentation. Boss is going to love these numbers 📊",
                "appeal": "This is a common expression, not a real threat.",
                "violation": False,
                "lang": "English",
                "difficulty": "medium",
                "reporter_trust": 0.38,
                "user_history_summary": "User history: Account age 500 days, no prior threats or abuse history.",
                "reporter_profile_summary": "Reporter trust score: 0.38. Reporter has filed several literal readings of idioms.",
                "similar_rulings_summary": "Similar rulings: Idiomatic workplace language without a real target is usually OVERTURN.",
            },
            "medium_004": {
                "post": "Vaccines are big pharma's way of controlling the population. Do your research!",
                "appeal": "I have the right to share my opinions about health.",
                "violation": True,
                "lang": "English",
                "difficulty": "medium",
                "reporter_trust": 0.66,
                "user_history_summary": "User history: Account age 780 days, one prior misinformation warning, otherwise normal activity.",
                "reporter_profile_summary": "Reporter trust score: 0.66. Usually reliable on health misinformation reports.",
                "similar_rulings_summary": "Similar rulings: Often UPHOLD when posts discourage trust in public-health measures using unsupported claims.",
            },
            "medium_005": {
                "post": "This diet helped me lose 30kg in 2 months! No exercise needed, just this one trick!",
                "appeal": "I was sharing my personal weight loss journey.",
                "violation": True,
                "lang": "English",
                "difficulty": "medium",
                "reporter_trust": 0.61,
                "user_history_summary": "User history: Account age 300 days, prior promotional-content warning.",
                "reporter_profile_summary": "Reporter trust score: 0.61. Fairly reliable but not definitive.",
                "similar_rulings_summary": "Similar rulings: Mixed, but exaggerated health-result claims paired with bait phrasing are frequently UPHOLD.",
            },
            "medium_006": {
                "post": "The election was stolen. Here is the proof the mainstream media won't show you.",
                "appeal": "I was sharing information that people deserve to know.",
                "violation": True,
                "lang": "English",
                "difficulty": "medium",
                "reporter_trust": 0.69,
                "user_history_summary": "User history: Account age 1100 days, previous civic misinformation warning.",
                "reporter_profile_summary": "Reporter trust score: 0.69. Reporter is generally credible on election-integrity topics.",
                "similar_rulings_summary": "Similar rulings: Unsupported conspiracy framing about election fraud is frequently UPHOLD.",
            },
            "medium_007": {
                "post": "I can't take this anymore. Every day feels the same and I'm exhausted.",
                "appeal": "I was venting about work stress, not expressing anything harmful.",
                "violation": False,
                "lang": "English",
                "difficulty": "medium",
                "reporter_trust": 0.44,
                "user_history_summary": "User history: Account age 840 days, no prior self-harm enforcement history.",
                "reporter_profile_summary": "Reporter trust score: 0.44. Mixed reliability on wellbeing reports.",
                "similar_rulings_summary": "Similar rulings: Distress alone is not always removed; policy often favors support-oriented handling unless intent is explicit.",
            },
            "medium_008": {
                "post": "This restaurant gave me food poisoning. AVOID at all costs! Worst place ever!",
                "appeal": "I was sharing a genuine consumer warning based on my experience.",
                "violation": False,
                "lang": "English",
                "difficulty": "medium",
                "reporter_trust": 0.34,
                "user_history_summary": "User history: Account age 1400 days, no prior harassment removals.",
                "reporter_profile_summary": "Reporter trust score: 0.34. Reporter often disputes negative reviews.",
                "similar_rulings_summary": "Similar rulings: Harsh consumer complaints are often allowed unless they include threats, doxxing, or fabricated allegations.",
            },
            "medium_009": {
                "post": "5G towers are spreading disease. Filmed one near a hospital. Coincidence?",
                "appeal": "I was raising awareness about public health concerns.",
                "violation": True,
                "lang": "English",
                "difficulty": "medium",
                "reporter_trust": 0.64,
                "user_history_summary": "User history: Account age 200 days, one prior misleading-health-content removal.",
                "reporter_profile_summary": "Reporter trust score: 0.64. Usually reliable in misinformation categories.",
                "similar_rulings_summary": "Similar rulings: Unsupported health-causation claims framed as fact are often UPHOLD.",
            },
            "medium_010": {
                "post": "My ex needs to stop contacting me. This is your final warning.",
                "appeal": "I was setting a boundary with someone harassing me.",
                "violation": False,
                "lang": "English",
                "difficulty": "medium",
                "reporter_trust": 0.46,
                "user_history_summary": "User history: Account age 1000 days, no prior threat removals, some interpersonal dispute reports.",
                "reporter_profile_summary": "Reporter trust score: 0.46. Mixed context; prior reports involved private disputes.",
                "similar_rulings_summary": "Similar rulings: Boundary-setting language may be allowed unless it includes a credible threat.",
            },

            # ── HARD CASES ─────────────────────────────────────────────────
            "hard_001": {
                "post": "यह सरकार पूरी तरह से भ्रष्ट है और इसे हटा दिया जाना चाहिए।",
                "appeal": "This is political speech, not hate speech.",
                "violation": False,
                "lang": "Hindi",
                "translation": "This government is completely corrupt and should be removed.",
                "translation_note": "Literal translation only. Political criticism may still require contextual judgment.",
                "difficulty": "hard",
                "reporter_trust": 0.52,
                "user_history_summary": "User history: Account age 640 days, no prior hate-speech removals.",
                "reporter_profile_summary": "Reporter trust score: 0.52. Mixed reliability in political-content reports.",
                "similar_rulings_summary": "Similar rulings: Criticism of governments is often allowed unless it targets protected groups or incites violence.",
            },
            "hard_002": {
                "post": "ഇവൻ ഇനി ഒരു ദിവസം കൂടി ജീവിക്കില്ല. ഞാൻ ഉറപ്പ് നൽകുന്നു.",
                "appeal": "This is just frustration, not a real threat.",
                "violation": True,
                "lang": "Malayalam",
                "translation": "This person will not live another day. I guarantee it.",
                "translation_note": "Translation suggests a direct threat; context does not soften the wording.",
                "difficulty": "hard",
                "reporter_trust": 0.75,
                "user_history_summary": "User history: Account age 210 days, prior warning for threatening language.",
                "reporter_profile_summary": "Reporter trust score: 0.75. Strong history of valid safety reports.",
                "similar_rulings_summary": "Similar rulings: Direct statements implying imminent killing are usually UPHOLD.",
            },
            "hard_003": {
                "post": "هؤلاء الناس لا ينتمون إلى بلدنا ويجب ترحيلهم جميعاً.",
                "appeal": "I was expressing my political views on immigration policy.",
                "violation": True,
                "lang": "Arabic",
                "translation": "These people do not belong in our country and should all be deported.",
                "translation_note": "Group-targeting language may overlap with political discussion; target framing matters.",
                "difficulty": "hard",
                "reporter_trust": 0.70,
                "user_history_summary": "User history: Account age 500 days, prior hateful-conduct warning.",
                "reporter_profile_summary": "Reporter trust score: 0.70. Strong record in hate-speech reporting.",
                "similar_rulings_summary": "Similar rulings: Group-exclusion rhetoric targeting people as outsiders is often UPHOLD.",
            },
            "hard_004": {
                "post": "இந்த அரசாங்கம் மக்களை ஏமாற்றுகிறது. நாம் எல்லோரும் போராட வேண்டும்.",
                "appeal": "This is a call for peaceful democratic protest, not incitement.",
                "violation": False,
                "lang": "Tamil",
                "translation": "This government is deceiving the people. We must all fight back.",
                "translation_note": "Phrase can be rhetorical or political; literal translation alone is not enough to infer violence.",
                "difficulty": "hard",
                "reporter_trust": 0.47,
                "user_history_summary": "User history: Account age 890 days, no prior violent-incitement removals.",
                "reporter_profile_summary": "Reporter trust score: 0.47. Mixed record on protest-related content.",
                "similar_rulings_summary": "Similar rulings: Protest language is often allowed absent explicit violent instruction.",
            },
            "hard_005": {
                "post": "1488 brothers rise up. These people are replacing us in our own neighborhoods. 🐸",
                "appeal": "I was expressing concerns about demographic changes in my area.",
                "violation": True,
                "lang": "English",
                "difficulty": "hard",
                "reporter_trust": 0.85,
                "user_history_summary": "User history: Account age 1600 days, verified account, prior warning for extremist symbolism.",
                "reporter_profile_summary": "Reporter trust score: 0.85. High accuracy on extremist-content reports.",
                "similar_rulings_summary": "Similar rulings: Coded extremist slogans and replacement rhetoric are commonly UPHOLD.",
            },
            "hard_006": {
                "post": "Orang-orang ini mencuri pekerjaan kita dan merusak budaya kita.",
                "appeal": "I was discussing economic impacts of immigration policy.",
                "violation": True,
                "lang": "Bahasa Indonesia",
                "translation": "These people are stealing our jobs and destroying our culture.",
                "translation_note": "Translation shows generalized hostility toward a group; exact referent remains important.",
                "difficulty": "hard",
                "reporter_trust": 0.65,
                "user_history_summary": "User history: Account age 420 days, prior warning for xenophobic generalization.",
                "reporter_profile_summary": "Reporter trust score: 0.65. Generally reliable.",
                "similar_rulings_summary": "Similar rulings: Broad demeaning claims about outsider groups are often UPHOLD.",
            },
            "hard_007": {
                "post": "Breaking: Graphic footage from conflict zone in Gaza. Warning — real casualties shown. Documentation only. #HumanRights",
                "appeal": "This is journalism and humanitarian documentation, not violent content.",
                "violation": False,
                "lang": "English",
                "difficulty": "hard",
                "reporter_trust": 0.43,
                "user_history_summary": "User history: Account age 950 days, no glorification-of-violence history.",
                "reporter_profile_summary": "Reporter trust score: 0.43. Reporter often flags graphic documentation without distinguishing context.",
                "similar_rulings_summary": "Similar rulings: Graphic documentation may remain allowed when clearly contextualized and non-glorifying.",
            },
            "hard_008": {
                "post": "আমাদের দেশ থেকে এই বিদেশিদের বের করে দাও। তারা আমাদের সংস্কৃতি নষ্ট করছে।",
                "appeal": "I was expressing my views on national identity and culture.",
                "violation": True,
                "lang": "Bengali",
                "translation": "Throw these foreigners out of our country. They are destroying our culture.",
                "translation_note": "Translation indicates exclusionary hostility toward outsiders as a group.",
                "difficulty": "hard",
                "reporter_trust": 0.72,
                "user_history_summary": "User history: Account age 610 days, prior hateful-conduct warning.",
                "reporter_profile_summary": "Reporter trust score: 0.72. Reliable in hate-related categories.",
                "similar_rulings_summary": "Similar rulings: Group-expulsion rhetoric is often UPHOLD.",
            },
            "hard_009": {
                "post": "Day 90 of recovery. Still fighting. Some days harder than others but I'm still here 💙 If anyone struggling please reach out.",
                "appeal": "This is a mental health recovery post, not harmful content.",
                "violation": False,
                "lang": "English",
                "difficulty": "hard",
                "reporter_trust": 0.26,
                "user_history_summary": "User history: Account age 720 days, no self-harm policy violations.",
                "reporter_profile_summary": "Reporter trust score: 0.26. Reporter frequently mistakes recovery-oriented posts for harmful intent.",
                "similar_rulings_summary": "Similar rulings: Recovery and support-oriented mental-health posts are often OVERTURN.",
            },
            "hard_010": {
                "post": "LEAKED: Internal CDC document proves vaccines cause autism in 1 in 3 children. Share before deleted!",
                "appeal": "People deserve access to information that authorities suppress.",
                "violation": True,
                "lang": "English",
                "difficulty": "hard",
                "reporter_trust": 0.81,
                "user_history_summary": "User history: Account age 350 days, prior misinformation warning, high repost volume.",
                "reporter_profile_summary": "Reporter trust score: 0.81. High accuracy in medical misinformation reports.",
                "similar_rulings_summary": "Similar rulings: Fabricated leak framing plus false vaccine claims is typically UPHOLD.",
            },
        }

        self.easy_cases = [k for k, v in self.cases.items() if v["difficulty"] == "easy"]
        self.medium_cases = [k for k, v in self.cases.items() if v["difficulty"] == "medium"]
        self.hard_cases = [k for k, v in self.cases.items() if v["difficulty"] == "hard"]

        self.current_case_id = None
        self._state = None

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        **kwargs
    ) -> ModerationObservation:
        task_id = kwargs.get("task_id", "easy_appeal")

        task_buckets = {
            "easy_appeal": self.easy_cases,
            "medium_appeal": self.medium_cases,
            "hard_appeal": self.hard_cases,
        }

        if task_id in task_buckets:
            bucket = task_buckets[task_id]
            if seed is not None:
                rng = random.Random(seed)
                self.current_case_id = rng.choice(bucket)
            elif episode_id:
                rng = random.Random(str(episode_id))
                self.current_case_id = rng.choice(bucket)
            else:
                # Deterministic rotation — reproducible but cycles through cases
                if not hasattr(self, "_task_counters"):
                    self._task_counters = {
                        "easy_appeal": 0,
                        "medium_appeal": 0,
                        "hard_appeal": 0,
                    }
                idx = self._task_counters[task_id] % len(bucket)
                self.current_case_id = bucket[idx]
                self._task_counters[task_id] += 1
        elif task_id in self.cases:
            self.current_case_id = task_id
        else:
            raise ValueError(f"Unknown task_id: {task_id}")

        case = self.cases[self.current_case_id]

        self._state = ModerationState(
            post_id=self.current_case_id,
            actual_violation=case["violation"],
            language=case["lang"],
            remaining_steps=8 if case["difficulty"] == "hard" else 6
        )

        return self._get_observation(reward=0.0, done=False)

    def step(
        self,
        action: ModerationAction,
        timeout_s: Optional[float] = None,
        **kwargs
    ) -> ModerationObservation:
        if self._state is None:
            raise RuntimeError("Environment not initialized. Call reset() first.")

        case = self.cases[self.current_case_id]
        difficulty = case["difficulty"]

        reward = 0.0
        done = False

        step_cost = {"easy": -0.05, "medium": -0.10, "hard": -0.15}
        reward += step_cost[difficulty]
        self._state.remaining_steps -= 1

        if action.action_type == "inspect_post":
            if not self._state.inspect_post_done:
                self._state.inspect_post_done = True
                reward += 0.05
                self._state.log.append(
                    f"Post inspected. Language: {self._state.language}. Content: '{case['post']}'"
                )
            else:
                self._state.log.append("inspect_post already used — no new information.")

        elif action.action_type == "fetch_user_history":
            if not self._state.history_extracted:
                self._state.history_extracted = True
                reward += 0.08
                self._state.log.append(case["user_history_summary"])
            else:
                self._state.log.append("fetch_user_history already used — no new information.")

        elif action.action_type == "fetch_reporter_profile":
            if not self._state.reporter_checked:
                self._state.reporter_checked = True
                reward += 0.08
                self._state.log.append(case["reporter_profile_summary"])
            else:
                self._state.log.append("fetch_reporter_profile already used — no new information.")

        elif action.action_type == "fetch_similar_rulings":
            if not self._state.similar_rulings_checked:
                self._state.similar_rulings_checked = True
                reward += 0.10
                self._state.log.append(case["similar_rulings_summary"])
            else:
                self._state.log.append("fetch_similar_rulings already used — no new information.")

        elif action.action_type == "request_translation":
            if self._state.language != "English":
                if not self._state.translation_requested:
                    self._state.translation_requested = True
                    reward += 0.15 if difficulty == "hard" else 0.10
                    translation = case.get("translation", "Translation not available.")
                    self._state.log.append(
                        f"Translation complete ({self._state.language} → English): '{translation}'"
                    )
                    if case.get("translation_note"):
                        self._state.log.append(f"Translator note: {case['translation_note']}")
                else:
                    self._state.log.append("Translation already requested — no new information.")
            else:
                self._state.log.append("Translation not needed — post is already in English.")

        elif action.action_type == "decide":
            done = True

            evidence_count = sum([
                1 if self._state.inspect_post_done else 0,
                1 if self._state.history_extracted else 0,
                1 if self._state.reporter_checked else 0,
                1 if self._state.similar_rulings_checked else 0,
                1 if (self._state.translation_requested or self._state.language == "English") else 0,
            ])

            if evidence_count < 2:
                reward -= 0.25
                self._state.log.append("Decision made with limited investigation evidence.")

            is_correct = (
                (action.decision == "UPHOLD" and self._state.actual_violation) or
                (action.decision == "OVERTURN" and not self._state.actual_violation)
            )

            correct_reward = {"easy": 1.0, "medium": 1.2, "hard": 1.5}
            false_positive = {"easy": -1.5, "medium": -1.8, "hard": -2.0}
            false_negative = {"easy": -1.0, "medium": -1.2, "hard": -1.5}

            if is_correct:
                reward += correct_reward[difficulty]
                self._state.log.append(f"Decision: {action.decision} — Correct.")
            else:
                if action.decision == "UPHOLD" and not self._state.actual_violation:
                    reward += false_positive[difficulty]
                    self._state.log.append("Decision: UPHOLD — Wrong. False positive.")
                else:
                    reward += false_negative[difficulty]
                    self._state.log.append("Decision: OVERTURN — Wrong. False negative.")

        else:
            self._state.log.append(f"Unknown action: {action.action_type}")

        if self._state.remaining_steps <= 0:
            done = True
            self._state.log.append("Episode ended: no remaining investigation steps.")

        return self._get_observation(reward=reward, done=done)

    @property
    def state(self) -> ModerationState:
        return self._state

    def _get_observation(self, reward: float, done: bool) -> ModerationObservation:
        case = self.cases[self.current_case_id]
        return ModerationObservation(
            post_content=case["post"],
            appeal_text=case["appeal"],
            available_actions=[
                "inspect_post",
                "fetch_user_history",
                "fetch_reporter_profile",
                "fetch_similar_rulings",
                "request_translation",
                "decide",
            ],
            investigation_log=self._state.log,
            remaining_steps=self._state.remaining_steps,
            reward=reward,
            done=done
        )