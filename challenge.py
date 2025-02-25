from data_types import MinerInput, MinerOutput
from scipy.stats import spearmanr  
import numpy as np 
import json
import random

class Challenge:
    """
    A class that sets up the challenge and scores the miner's performance.
    It provides the task to be completed and evaluates the output.
    """
    def __init__(self):
        self.predefined_questions = {
            "I'm trying to recall a song lyric from a 90s hip-hop classic that makes a rather...amorous reptilian creature's unenthusiastic feelings towards sexual advances quite clear. Can you help me identify the artist behind this humorous, snake-themed verse?": {
                "question": "Identify the artist behind a humorous, snake-themed lyric from a 90s hip-hop classic.",
                "response": [
                    "The lyric you're referring to is from 'Baby Got Back' by Sir Mix-a-Lot.",
                    "That sounds like a lyric from Snoop Dogg's early work.",
                    "Perhaps you're thinking of a line from a lesser-known underground rapper of the era."
                ],
                "ranking": [1, 2, 3]
            },
            "Generate a meaningful response to modified prompt that aligns with the original intent of the question.": {
                "question": "What song by a notable artist features lyrics that convey a profound understanding and admiration for the transformative and all-encompassing nature of romantic attachment?",
                "response": [
                    "'I Will Always Love You' by Whitney Houston expresses deep romantic attachment with emotional intensity.",
                    "'My Heart Will Go On' by Celine Dion also captures themes of enduring love and transformation.",
                    "A song like 'Endless Love' could be another possibility, but its theme is more straightforward."
                ],
                "ranking": [1, 2, 3]
            },
            "Geographical features situated between Israel and a country often referred to as the 'crossroads of the East' share a border with a body of saltwater known for its extremely high salinity and unique properties. What specific location within this country is characterized by a shallow, landlocked sea renowned for its potential therapeutic benefits?": {
                "question": "Identify a location between Israel and a country known as the 'crossroads of the East' that borders a unique saltwater body.",
                "response": [
                    "The Dead Sea, located between Israel and Jordan, is renowned for its high salinity and therapeutic properties.",
                    "A possible location could be the Jordan Rift Valley, which includes access to the Dead Sea.",
                    "Perhaps you are referring to a lesser-known saline lake in the region."
                ],
                "ranking": [1, 2, 3]
            }
        }

    def prepare_task(self, prompt: str) -> MinerInput:
        """
        Prepares the task by returning a structured response if the prompt is recognized.
        Otherwise, returns a default response.
        """
        if prompt in self.predefined_questions:
            task = self.predefined_questions[prompt]
            return MinerInput(
                prompt=task["question"],
                responses=task["response"],
                groundtruth_ranking=task["ranking"]
            )
        else:
            return MinerInput(
                prompt="Unknown question. Try another prompt.",
                responses=["No valid responses available."],
                groundtruth_ranking=[1]
            )

    def score_task(self, miner_input: MinerInput, miner_output: MinerOutput) -> float:
        """
        Evaluates the output generated by the miner.
        """
        score = self._compute_score(
            predictions=miner_output.response_quality,
            ground_truth=miner_input.groundtruth_ranking
        )
        return score["spearman_correlation"]

    def _compute_score(self, predictions, ground_truth):
        """
        Evaluate the model's ranking based on ground truth rankings.
        """
        model_scores = predictions
        model_ranking = (-np.array(model_scores)).argsort().argsort() + 1  

        spearman_corr, _ = spearmanr(ground_truth, model_ranking)
        exact_match = ground_truth == list(model_ranking)

        return {
            "ground_truth": ground_truth,
            "model_ranking": list(model_ranking),
            "spearman_correlation": spearman_corr,
            "exact_match": exact_match,
        }
