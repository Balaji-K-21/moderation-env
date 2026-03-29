from fastapi import FastAPI
from pydantic import BaseModel
from server.env import ModerationEnv
from models import ModerationAction

app = FastAPI()

class ResetRequest(BaseModel):
    task_id: str = "easy_appeal"

class StepRequest(BaseModel):
    action: ModerationAction

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/reset")
def reset_env(req: ResetRequest):
    app.state.env = ModerationEnv()  # Fresh instance per reset
    obs = app.state.env.reset(task_id=req.task_id)
    return {"observation": obs.model_dump()}

@app.post("/step")
def step_env(req: StepRequest):
    obs = app.state.env.step(req.action)
    return {"observation": obs.model_dump()}

@app.get("/state")
def get_state():
    return app.state.env.state.model_dump()