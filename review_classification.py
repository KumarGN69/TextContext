from custom_llm import LLMModel
import pandas as pd
import os, dotenv

class ReviewClassifier:
    def __init__(self):
        dotenv.load_dotenv()
        self.model = LLMModel()
        self.client = self.model.getclientinterface()
        self.MODEL = os.getenv('INFERENCE_MODEL')
        self.classifiers = (f"Audio Issues, Video Issues,User Experience, Service, Support, Others, Technical,"
                            f"Voice Quality, Bluetooth, WiFi, Call drop ")
        self.output_criteria = (f"Strictly provide only the category names as comma separated list without "
                                f"any explanation or qualification")

    def classifyPositiveReviews(self):
        try:
            df= pd.read_json("./reddit_positive_reviews.json")
            comment_list = [df['user_review'][record] for record in range(0,df['user_review'].size)]
            comment_classification =[]
            for comment in comment_list:
                classifier = self.client.generate(
                    model=self.MODEL,
                    prompt=f"Classify the {comment} using the categories {self.classifiers}.{self.output_criteria} "
                )
                sentiment = "Positive"
                comment_classification.append({
                    "review": {
                        "sentiment": sentiment,
                        "categories": [classifier.response],
                        "user_review": comment
                    }
                })
            if comment_classification:
                df = pd.DataFrame(comment_classification)
                json_file_name = "reddit_positive_review_classification.json"
                df.to_json(json_file_name, index=False)
                csv_file_name = "reddit_positive_review_classification.csv"
                df.to_csv(csv_file_name, index=False)
            else:
                print(" No reviews found!")

        except Exception as e:
            print(f"Error fetching reviews: {e}")


    def classifyNegativeReviews(self):
        try:
            df = pd.read_json("./reddit_negative_reviews.json")
            comment_list = [df['user_review'][record] for record in range(0, df['user_review'].size)]
            comment_classification = []
            for comment in comment_list:
                classifier = self.client.generate(
                    model=self.MODEL,
                    prompt=f"Classify the {comment} using the categories {self.classifiers}.{self.output_criteria} "
                )
                sentiment = "Negative"
                comment_classification.append({
                    "review": {
                        "sentiment": sentiment,
                        "categories": [classifier.response],
                        "user_review": comment
                    }
                })

            if comment_classification:
                df = pd.DataFrame(comment_classification)
                json_file_name = "reddit_negative_review_classification.json"
                df.to_json(json_file_name, index=False)
                csv_file_name = "reddit_negative_review_classification.csv"
                df.to_csv(csv_file_name, index=False)
            else:
                print(" No reviews found!")

        except Exception as e:
            print(f"Error fetching reviews: {e}")
            # create csv and json files for neutral comments

    def classifyNeutralReviews(self):
        try:
            df = pd.read_json("./reddit_neutral_reviews.json")
            comment_list = [df['user_review'][record] for record in range(0, df['user_review'].size)]
            comment_classification = []
            for comment in comment_list:
                classifier = self.client.generate(
                    model=self.MODEL,
                    prompt=f"Classify the {comment} using the categories {self.classifiers}.{self.output_criteria} "

                )
                sentiment = "Neutral"
                comment_classification.append({
                    "review": {
                        "sentiment": sentiment,
                        "categories": [classifier.response],
                        "user_review": comment
                    }
                })

            if comment_classification:
                df = pd.DataFrame(comment_classification)
                json_file_name = "reddit_neutral_review_classification.json"
                df.to_json(json_file_name, index=False)
                csv_file_name = "reddit_neutral_review_classification.csv"
                df.to_csv(csv_file_name, index=False)
            else:
                print(" No reviews found!")

        except Exception as e:
            print(f"Error fetching reviews: {e}")



