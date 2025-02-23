from custom_llm import LLMModel
import pandas as pd
import os, dotenv

class ReviewClassifier:
    """

    """
    def __init__(self):
        dotenv.load_dotenv()
        self.model = LLMModel()
        self.client = self.model.getclientinterface()
        self.MODEL = os.getenv('INFERENCE_MODEL')
        # self.classifiers = (f"Audio Issues, Video Issues,User Experience, Service, Support, Others, Technical,"
        #                     f"Voice Quality, Bluetooth, WiFi, Call drop ")
        self.classifiers = {
            "Audio Issues": ["audio", "sound"],
            "Video Issues": ["video", "display"],
            "User Experience": ["experience", "user"],
            "Service": ["service", "support"],
            "Support": ["support", "help"],
            "Others": ["other"],
            "Technical": ["technical", "tech"],
            "Voice Quality": ["voice", "call quality"],
            "Bluetooth": ["bluetooth"],
            "WiFi": ["wifi", "wireless"],
            "Call drop": ["call drop", "dropped call"]
        }
        self.output_criteria = (f"Return only category names from {self.classifiers} as a comma-separated list, "
                                f"ensuring: 1. No new lines or extra white spaces. "
                                f"2. No additional words, explanations, or qualifiers. "
                                f"3. Map only to the relevant categories from the provided categories: {self.classifiers} ."
                                f"4. If none of the categories are relevant then use None")

    def classifyReviews(self,sentiment:str):
        """
        """
        try:
            df= pd.read_json(f"./reddit_{sentiment}_reviews.json")
            comment_list = [df['user_review'][record] for record in range(0,df['user_review'].size)]
            print(f"Classification of {sentiment} reviews in progress")
            comment_classification = self.classifyAndUpdate(
                comment_list=comment_list,
                sentiment = sentiment
                )
  
            print(f"Classification of {sentiment} reviews complete ")
            if comment_classification:
                self.saveToFile(
                    sentiment=sentiment,
                    comment_classification=comment_classification
                    )
            else:
                print(" No reviews found!")

        except Exception as e:
            print(f"Error fetching reviews: {e}")


    def classifyAndUpdate(self, comment_list:list,sentiment:str):
        """
        """
        classifications =[]
        for comment in comment_list:
                classifier = self.client.generate(
                    model=self.MODEL,
                    prompt=f"Classify the {comment}.Use only the categories from {self.classifiers}.{self.output_criteria} "
                )
                sentiment = sentiment
                classifications.append({
                        "sentiment": sentiment,
                        "categories": [classifier.response],
                        "user_review": comment
                })
        return classifications    
    
    def saveToFile(self,sentiment:str,comment_classification:list):
        """
        """
        df = pd.DataFrame(comment_classification)
        json_file_name = f"reddit_{sentiment}_review_classification.json"
        df.to_json(json_file_name, index=False)
        csv_file_name = f"reddit_{sentiment}_review_classification.csv"
        df.to_csv(csv_file_name, index=False)


