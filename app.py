from fastapi import FastAPI
from challenge import Challenge
from data_types import MinerInput, MinerOutput

# Create FastAPI instance
app = FastAPI()

# Create Challenge instance
challenge = Challenge()

@app.get("/task")
def get_task(prompt: str):
    """
    Get a challenge task by passing a prompt.
    """
    task = challenge.prepare_task(prompt)
    return task.dict()  # Convert Pydantic model to dictionary

@app.post("/score")
def score_task(miner_input: MinerInput, miner_output: MinerOutput):
    """
    Evaluate a user's ranking response.
    """
    return {"score": challenge.score_task(miner_input, miner_output)}

@app.get("/health")
def health():
    """
    Simple health check.
    """
    return {"status": "healthy"}
