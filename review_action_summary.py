from custom_llm import LLMModel
import pandas as pd
import os, dotenv

class ReviewSummarizer():
    """

    """
    def __init__(self):
        dotenv.load_dotenv()
        self.model = LLMModel()
        self.client = self.model.getclientinterface()
        self.MODEL = os.getenv('INFERENCE_MODEL')

    def summarizeReviews(self,sentiment:str):
        """
        """
        try:
            df = pd.read_json(f"reddit_{sentiment}_review_classification.json")
            pass
        except Exception as e:
            print(f"Error fetching reviews: {e}")
            pass

    def saveToFile(self):
        """
        """
        pass