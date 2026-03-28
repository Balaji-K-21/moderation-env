from typing import List, Optional, Literal
from pydantic import Field
from openenv.core.env_server import Action, Observation, State

class ModerationObservation(Observation):
    post_content: str = Field(description="The text of the flagged post")
    appeal_text: str = Field(description="The user's reason for appealing the block")
    available_actions: List[str] = Field(description="List of allowed actions")
    investigation_log: List[str] = Field(default_factory=list, description="History of evidence gathered")
    remaining_steps: int = Field(description="Remaining actions")
    reward: float = Field(default=0.0, description="Reward for the last action")
    done: bool = Field(default=False, description="Whether the episode is over")

class ModerationAction(Action):
    action_type: Literal[
        "inspect_post",
        "fetch_user_history",
        "fetch_reporter_profile",
        "fetch_similar_rulings",
        "request_translation",
        "decide"
    ]
    decision: Optional[Literal["UPHOLD", "OVERTURN"]] = Field(default=None)

class ModerationState(State):
    post_id: str = Field(description="ID of the current case")
    actual_violation: bool = Field(description="Ground truth — hidden from agent")
    language: str = Field(default="English", description="Language of the post")
    inspect_post_done: bool = Field(default=False)
    history_extracted: bool = Field(default=False)
    reporter_checked: bool = Field(default=False)
    similar_rulings_checked: bool = Field(default=False)
    translation_requested: bool = Field(default=False)
    remaining_steps: int = Field(default=6)
    log: List[str] = Field(default_factory=list)