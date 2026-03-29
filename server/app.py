from openenv.core.env_server import create_fastapi_app
from models import ModerationObservation, ModerationAction
from server.env import ModerationEnv

app = create_fastapi_app(
    env=ModerationEnv,
    action_cls=ModerationAction,
    observation_cls=ModerationObservation
)