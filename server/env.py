from typing import Optional
from openenv.core.env_server import Environment
from models import ModerationObservation, ModerationAction, ModerationState


class ModerationEnv(Environment[ModerationAction, ModerationObservation, ModerationState]):
    # Shared state across requests
    _shared_state: Optional[ModerationState] = None
    _shared_case_id: Optional[str] = None

    def __init__(self):
        super().__init__()

        self.cases = {
            # ── EASY CASES ─────────────────────────────────────────────────
            "easy_001": {
                "post": "BUY CHEAP PHARMA NOW! LINK IN BIO!!!",
                "appeal": "This is not spam, I am just sharing a deal.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.9,
                "difficulty": "easy"
            },
            "easy_002": {
                "post": "MAKE $5000 A DAY FROM HOME! NO EXPERIENCE NEEDED! CLICK HERE!!!",
                "appeal": "I am just sharing a business opportunity.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.85,
                "difficulty": "easy"
            },
            "easy_003": {
                "post": "FREE iPhone 15 giveaway! Just send $50 processing fee to claim yours!",
                "appeal": "This is a legitimate giveaway promotion.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.9,
                "difficulty": "easy"
            },
            "easy_004": {
                "post": "Just finished my morning run! 5km in 28 minutes, new personal best!",
                "appeal": "I was just sharing my fitness progress, this is not spam.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.1,
                "difficulty": "easy"
            },
            "easy_005": {
                "post": "Happy birthday to my amazing mom! Love you to the moon and back 🎂❤️",
                "appeal": "This is a personal birthday message, not a violation.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.05,
                "difficulty": "easy"
            },
            "easy_006": {
                "post": "URGENT: Your account has been compromised! Click this link NOW to secure it: bit.ly/fake123",
                "appeal": "I was trying to help people secure their accounts.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.95,
                "difficulty": "easy"
            },
            "easy_007": {
                "post": "Lost my dog near Central Park today. Brown labrador, answers to Max. Please share!",
                "appeal": "I was just trying to find my lost pet, not violating any rules.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.05,
                "difficulty": "easy"
            },
            "easy_008": {
                "post": "Get rich quick with crypto! 1000% returns guaranteed! DM me NOW before it's too late!!!",
                "appeal": "Cryptocurrency investment is legal and I was sharing opportunities.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.88,
                "difficulty": "easy"
            },
            "easy_009": {
                "post": "Beautiful sunset at the beach today 🌅 Nature is amazing!",
                "appeal": "This is just a photo of a sunset, completely harmless.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.08,
                "difficulty": "easy"
            },
            "easy_010": {
                "post": "Buy followers cheap! 10000 followers for $5! Real accounts guaranteed!",
                "appeal": "This is a marketing service, not against any rules.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.92,
                "difficulty": "easy"
            },
            "easy_011": {
                "post": "Just adopted a rescue kitten! Meet Luna 🐱 She's already ruling the house!",
                "appeal": "Pet adoption post is not a violation of any kind.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.03,
                "difficulty": "easy"
            },
            "easy_012": {
                "post": "FREE gift cards! Like and share this post to win! 100% real no scam!!!",
                "appeal": "This is a genuine promotional giveaway for my followers.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.87,
                "difficulty": "easy"
            },
            "easy_013": {
                "post": "Cooked homemade biryani today! Recipe in the comments 🍛",
                "appeal": "Sharing a recipe is not a policy violation.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.04,
                "difficulty": "easy"
            },
            "easy_014": {
                "post": "VERIFIED HACK: Get unlimited free gems in any game! Download now: fakesite.xyz",
                "appeal": "I was sharing useful gaming tips with the community.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.91,
                "difficulty": "easy"
            },
            "easy_015": {
                "post": "Proud of my daughter for graduating today! First in our family to get a degree!",
                "appeal": "This is a personal family celebration post.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.02,
                "difficulty": "easy"
            },

            # ── MEDIUM CASES ───────────────────────────────────────────────
            "medium_001": {
                "post": "I hate how everyone in this group acts like a child.",
                "appeal": "I was expressing frustration, not harassing anyone.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.3,
                "difficulty": "medium"
            },
            "medium_002": {
                "post": "These politicians are destroying our country. They should all be thrown out.",
                "appeal": "This is political opinion, protected free speech.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.35,
                "difficulty": "medium"
            },
            "medium_003": {
                "post": "I want to kill this presentation. Boss is going to love these numbers 📊",
                "appeal": "This is a common expression, not a real threat.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.25,
                "difficulty": "medium"
            },
            "medium_004": {
                "post": "Vaccines are big pharma's way of controlling the population. Do your research!",
                "appeal": "I have the right to share my opinions about health.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.65,
                "difficulty": "medium"
            },
            "medium_005": {
                "post": "This diet helped me lose 30kg in 2 months! No exercise needed, just this one trick!",
                "appeal": "I was sharing my personal weight loss journey.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.6,
                "difficulty": "medium"
            },
            "medium_006": {
                "post": "The election was stolen. Here is the proof the mainstream media won't show you.",
                "appeal": "I was sharing information that people deserve to know.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.7,
                "difficulty": "medium"
            },
            "medium_007": {
                "post": "I can't take this anymore. Every day feels the same and I'm exhausted.",
                "appeal": "I was venting about work stress, not expressing anything harmful.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.4,
                "difficulty": "medium"
            },
            "medium_008": {
                "post": "This restaurant gave me food poisoning. AVOID at all costs! Worst place ever!",
                "appeal": "I was sharing a genuine consumer warning based on my experience.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.3,
                "difficulty": "medium"
            },
            "medium_009": {
                "post": "5G towers are spreading disease. Filmed one near a hospital. Coincidence?",
                "appeal": "I was raising awareness about public health concerns.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.65,
                "difficulty": "medium"
            },
            "medium_010": {
                "post": "My ex needs to stop contacting me. This is your final warning.",
                "appeal": "I was setting a boundary with someone harassing me.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.45,
                "difficulty": "medium"
            },
            "medium_011": {
                "post": "Natural herbs can cure cancer. Doctors don't want you to know this!",
                "appeal": "Traditional medicine has been used for thousands of years.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.7,
                "difficulty": "medium"
            },
            "medium_012": {
                "post": "I'm done with this toxic workplace. HR protects abusers not victims.",
                "appeal": "I was sharing my experience with workplace harassment.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.25,
                "difficulty": "medium"
            },
            "medium_013": {
                "post": "Climate change is a hoax invented by globalists to control energy prices.",
                "appeal": "I have the right to question scientific consensus.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.6,
                "difficulty": "medium"
            },
            "medium_014": {
                "post": "Anyone else think their neighbor is running an illegal operation? Mine has people coming and going all night.",
                "appeal": "I was expressing concern about suspicious activity in my neighborhood.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.35,
                "difficulty": "medium"
            },
            "medium_015": {
                "post": "This influencer is a fraud. She photoshops all her photos and lies about her lifestyle.",
                "appeal": "I was exposing dishonest content creators for public awareness.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.3,
                "difficulty": "medium"
            },

            # ── HARD CASES ─────────────────────────────────────────────────
            "hard_001": {
                "post": "यह सरकार पूरी तरह से भ्रष्ट है और इसे हटा दिया जाना चाहिए।",
                "appeal": "This is political speech, not hate speech.",
                "violation": False,
                "lang": "Hindi",
                "translation": "This government is completely corrupt and should be removed.",
                "reporter_trust": 0.5,
                "difficulty": "hard"
            },
            "hard_002": {
                "post": "ഇവൻ ഇനി ഒരു ദിവസം കൂടി ജീവിക്കില്ല. ഞാൻ ഉറപ്പ് നൽകുന്നു.",
                "appeal": "This is just frustration, not a real threat.",
                "violation": True,
                "lang": "Malayalam",
                "translation": "This person will not live another day. I guarantee it.",
                "reporter_trust": 0.75,
                "difficulty": "hard"
            },
            "hard_003": {
                "post": "هؤلاء الناس لا ينتمون إلى بلدنا ويجب ترحيلهم جميعاً.",
                "appeal": "I was expressing my political views on immigration policy.",
                "violation": True,
                "lang": "Arabic",
                "translation": "These people do not belong in our country and should all be deported.",
                "reporter_trust": 0.7,
                "difficulty": "hard"
            },
            "hard_004": {
                "post": "இந்த அரசாங்கம் மக்களை ஏமாற்றுகிறது. நாம் எல்லோரும் போராட வேண்டும்.",
                "appeal": "This is a call for peaceful democratic protest, not incitement.",
                "violation": False,
                "lang": "Tamil",
                "translation": "This government is deceiving the people. We must all fight back.",
                "reporter_trust": 0.45,
                "difficulty": "hard"
            },
            "hard_005": {
                "post": "1488 brothers rise up. These people are replacing us in our own neighborhoods. 🐸",
                "appeal": "I was expressing concerns about demographic changes in my area.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.85,
                "difficulty": "hard"
            },
            "hard_006": {
                "post": "Orang-orang ini mencuri pekerjaan kita dan merusak budaya kita.",
                "appeal": "I was discussing economic impacts of immigration policy.",
                "violation": True,
                "lang": "Bahasa Indonesia",
                "translation": "These people are stealing our jobs and destroying our culture.",
                "reporter_trust": 0.65,
                "difficulty": "hard"
            },
            "hard_007": {
                "post": "Breaking: Graphic footage from conflict zone in Gaza. Warning — real casualties shown. Documentation only. #HumanRights",
                "appeal": "This is journalism and humanitarian documentation, not violent content.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.4,
                "difficulty": "hard"
            },
            "hard_008": {
                "post": "আমাদের দেশ থেকে এই বিদেশিদের বের করে দাও। তারা আমাদের সংস্কৃতি নষ্ট করছে।",
                "appeal": "I was expressing my views on national identity and culture.",
                "violation": True,
                "lang": "Bengali",
                "translation": "Throw these foreigners out of our country. They are destroying our culture.",
                "reporter_trust": 0.7,
                "difficulty": "hard"
            },
            "hard_009": {
                "post": "Day 90 of recovery. Still fighting. Some days harder than others but I'm still here 💙 If anyone struggling please reach out.",
                "appeal": "This is a mental health recovery post, not harmful content.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.1,
                "difficulty": "hard"
            },
            "hard_010": {
                "post": "LEAKED: Internal CDC document proves vaccines cause autism in 1 in 3 children. Share before deleted!",
                "appeal": "People deserve access to information that authorities suppress.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.88,
                "difficulty": "hard"
            },
            "hard_011": {
                "post": "இந்த தடுப்பூசி குழந்தைகளுக்கு ஆபத்தானது. எனது மகனுக்கு பக்க விளைவுகள் வந்தன.",
                "appeal": "I was sharing my child's vaccine side effects as a warning to parents.",
                "violation": False,
                "lang": "Tamil",
                "translation": "This vaccine is dangerous for children. My son experienced side effects.",
                "reporter_trust": 0.35,
                "difficulty": "hard"
            },
            "hard_012": {
                "post": "These globalists are running a worldwide child trafficking network. Follow the money. #SaveTheChildren",
                "appeal": "Child safety awareness is important and I was spreading awareness.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.8,
                "difficulty": "hard"
            },
            "hard_013": {
                "post": "मैं अब और नहीं जी सकता। सब कुछ बेकार लग रहा है।",
                "appeal": "I was just expressing frustration about my work situation.",
                "violation": True,
                "lang": "Hindi",
                "translation": "I cannot live anymore. Everything seems pointless.",
                "reporter_trust": 0.6,
                "difficulty": "hard"
            },
            "hard_014": {
                "post": "Injection sites for heroin users save lives. Here is how supervised consumption works and why cities need them.",
                "appeal": "This is harm reduction public health information from a verified NGO.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.3,
                "difficulty": "hard"
            },
            "hard_015": {
                "post": "கடவுளை நம்பாதவர்கள் நரகத்தில் எரிவார்கள். இது உண்மை.",
                "appeal": "I was sharing my sincere religious beliefs.",
                "violation": False,
                "lang": "Tamil",
                "translation": "Those who do not believe in God will burn in hell. This is the truth.",
                "reporter_trust": 0.4,
                "difficulty": "hard"
            },
        }

        self.easy_cases = [k for k, v in self.cases.items() if v["difficulty"] == "easy"]
        self.medium_cases = [k for k, v in self.cases.items() if v["difficulty"] == "medium"]
        self.hard_cases = [k for k, v in self.cases.items() if v["difficulty"] == "hard"]

    @property
    def current_case_id(self) -> Optional[str]:
        return self.__class__._shared_case_id

    @current_case_id.setter
    def current_case_id(self, value: Optional[str]) -> None:
        self.__class__._shared_case_id = value

    @property
    def _state(self) -> Optional[ModerationState]:
        return self.__class__._shared_state

    @_state.setter
    def _state(self, value: Optional[ModerationState]) -> None:
        self.__class__._shared_state = value

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        **kwargs
    ) -> ModerationObservation:
        task_id = kwargs.get("task_id", "easy_appeal")

        task_map = {
            "easy_appeal": "easy_001",
            "medium_appeal": "medium_001",
            "hard_appeal": "hard_001",
        }

        if task_id in task_map:
            self.current_case_id = task_map[task_id]
        elif task_id in self.cases:
            self.current_case_id = task_id
        else:
            raise ValueError(f"Unknown task_id: {task_id}")

        case = self.cases[self.current_case_id]

        self._state = ModerationState(
            post_id=self.current_case_id,
            actual_violation=case["violation"],
            language=case["lang"],
            remaining_steps=8 if case["difficulty"] == "hard" else 6,
        )

        return self._get_observation(reward=0.0, done=False)

    def step(
        self,
        action: ModerationAction,
        timeout_s: Optional[float] = None,
        **kwargs
    ) -> ModerationObservation:
        if self._state is None or self.current_case_id is None:
            raise RuntimeError("Environment not initialized. Call reset() first.")

        case = self.cases[self.current_case_id]
        difficulty = case["difficulty"]

        reward = 0.0
        done = False

        step_cost = {"easy": -0.05, "medium": -0.1, "hard": -0.15}
        reward += step_cost[difficulty]
        self._state.remaining_steps -= 1

        if action.action_type == "inspect_post":
            if not self._state.inspect_post_done:
                self._state.inspect_post_done = True
                self._state.log.append(
                    f"Post inspected. Language: {self._state.language}. "
                    f"Content: '{case['post']}'"
                )
            else:
                self._state.log.append("inspect_post already used — no new information.")

        elif action.action_type == "fetch_user_history":
            if not self._state.history_extracted:
                self._state.history_extracted = True
                if case["violation"]:
                    self._state.log.append(
                        "User history: Account age 3 days, 2 prior violations, unverified."
                    )
                else:
                    self._state.log.append(
                        "User history: Account age 1200 days, 0 prior violations, verified."
                    )
            else:
                self._state.log.append("fetch_user_history already used — no new information.")

        elif action.action_type == "fetch_reporter_profile":
            if not self._state.reporter_checked:
                self._state.reporter_checked = True
                trust = case["reporter_trust"]
                if trust >= 0.7:
                    self._state.log.append(
                        f"Reporter trust score: {trust}. Reporter has strong history of valid reports."
                    )
                elif trust <= 0.4:
                    self._state.log.append(
                        f"Reporter trust score: {trust}. Reporter has history of filing false reports."
                    )
                else:
                    self._state.log.append(
                        f"Reporter trust score: {trust}. Reporter history is mixed — proceed carefully."
                    )
            else:
                self._state.log.append("fetch_reporter_profile already used — no new information.")

        elif action.action_type == "fetch_similar_rulings":
            if not self._state.similar_rulings_checked:
                self._state.similar_rulings_checked = True
                if case["violation"]:
                    self._state.log.append(
                        "Similar rulings: 3 of 3 precedent cases were UPHOLD for this content type."
                    )
                else:
                    self._state.log.append(
                        "Similar rulings: 2 of 3 precedent cases were OVERTURN for this content type."
                    )
            else:
                self._state.log.append("fetch_similar_rulings already used — no new information.")

        elif action.action_type == "request_translation":
            if self._state.language != "English":
                if not self._state.translation_requested:
                    self._state.translation_requested = True
                    translation = case.get("translation", "Translation not available.")
                    reward += 0.3 if difficulty == "hard" else 0.2
                    self._state.log.append(
                        f"Translation complete ({self._state.language} → English): '{translation}'"
                    )
                else:
                    self._state.log.append("Translation already requested — no new information.")
            else:
                self._state.log.append("Translation not needed — post is already in English.")

        elif action.action_type == "decide":
            done = True
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

        if self._state.remaining_steps <= 0:
            done = True

        return self._get_observation(reward=reward, done=done)

    @property
    def state(self) -> ModerationState:
        if self._state is None:
            raise RuntimeError("Environment not initialized. Call reset() first.")
        return self._state

    def _get_observation(self, reward: float, done: bool) -> ModerationObservation:
        if self._state is None or self.current_case_id is None:
            raise RuntimeError("Environment not initialized. Call reset() first.")

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
                "decide"
            ],
            investigation_log=self._state.log,
            remaining_steps=self._state.remaining_steps,
            reward=reward,
            done=done
        )