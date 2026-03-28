from typing import Optional
from openenv.core.env_server import Environment
from models import ModerationObservation, ModerationAction, ModerationState


class ModerationEnv(Environment[ModerationAction, ModerationObservation, ModerationState]):
    def __init__(self):
        super().__init__()
        self.cases = {
            "easy_appeal": {
                "post": "BUY CHEAP PHARMA NOW! LINK IN BIO!!!",
                "appeal": "This is not spam, I am just sharing a deal.",
                "violation": True,
                "lang": "English",
                "reporter_trust": 0.9
            },
            "medium_appeal": {
                "post": "I hate how everyone in this group acts like a child.",
                "appeal": "I was expressing frustration, not harassing anyone.",
                "violation": False,
                "lang": "English",
                "reporter_trust": 0.3
            },
            "hard_appeal": {
                "post": "यह सरकार पूरी तरह से भ्रष्ट है और इसे हटा दिया जाना चाहिए।",
                "appeal": "This is political speech, not hate speech.",
                "violation": False,
                "lang": "Hindi",
                "reporter_trust": 0.5
            }
        }
        self.current_case_id = None
        self._state = None

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        **kwargs
    ) -> ModerationObservation:
        task_id = kwargs.get("task_id", "easy_appeal")
        self.current_case_id = task_id
        case = self.cases[task_id]

        self._state = ModerationState(
            post_id=task_id,
            actual_violation=case["violation"],
            language=case["lang"],
            remaining_steps=8 if task_id == "hard_appeal" else 6
        )

        return self._get_observation(reward=0.0, done=False)

    def step(
        self,
        action: ModerationAction,
        timeout_s: Optional[float] = None,
        **kwargs
    ) -> ModerationObservation:

        # Auto-reset if state is None
        if self._state is None:
            self.reset(task_id="easy_appeal")

        reward = 0.0
        done = False

        self._state.remaining_steps -= 1
        reward -= 0.1

        case = self.cases[self.current_case_id]

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
                        f"Reporter trust score: {trust}. Reporter has a strong history of valid reports."
                    )
                elif trust <= 0.4:
                    self._state.log.append(
                        f"Reporter trust score: {trust}. Reporter has a history of filing false reports."
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
                    reward += 0.2
                    self._state.log.append(
                        f"Translation complete ({self._state.language} → English): "
                        "'This government is completely corrupt and should be removed.'"
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
            if is_correct:
                reward += 1.0
                self._state.log.append(f"Decision: {action.decision} — Correct.")
            else:
                if action.decision == "UPHOLD" and not self._state.actual_violation:
                    reward -= 1.5
                    self._state.log.append("Decision: UPHOLD — Wrong. False positive.")
                else:
                    reward -= 1.0
                    self._state.log.append("Decision: OVERTURN — Wrong. False negative.")

        if self._state.remaining_steps <= 0:
            done = True

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
                "decide"
            ],
            investigation_log=self._state.log,
            remaining_steps=self._state.remaining_steps,
            reward=reward,
            done=done
        )