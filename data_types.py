from pydantic import BaseModel
from typing import List, Optional

class MinerInput(BaseModel):
    """
    Represents the input data for the challenge.
    Includes a prompt, a list of responses to evaluate, 
    and the ground truth ranking for those responses.
    """
    prompt: str
    responses: List[str]
    groundtruth_ranking: Optional[List[int]] = None 

class MinerOutput(BaseModel):
    """
    Represents the miner's output for the challenge.
    Contains the quality scores assigned to the responses.
    """
    response_quality: List[float]  # Quality scores for each response, higher is better
