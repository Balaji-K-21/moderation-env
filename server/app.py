from openenv.core.env_server import create_fastapi_app
from models import ModerationObservation, ModerationAction
from server.env import ModerationEnv

app = create_fastapi_app(
    env=ModerationEnv,
    action_cls=ModerationAction,
    observation_cls=ModerationObservation
)

def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()