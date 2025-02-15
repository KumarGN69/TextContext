from custom_llm import LLMModel
import pandas as pd
import os, dotenv

class ReviewClassifier:
    def __init__(self):
        dotenv.load_dotenv()
        self.model = LLMModel()
        self.client = self.model.getclientinterface()
        self.MODEL = os.getenv('INFERENCE_MODEL')

    def classifyPositiveReviews(self):
        try:
            df= pd.read_json("./reddit_positive_reviews.json")
            comment_list = [df['user_review'][record] for record in range(0,df['user_review'].size)]
            comment_classification =[]
            for comment in comment_list:
                classifier = self.client.generate(
                    model=self.MODEL,
                    prompt=f"Classify the entire {comment} into one of the following dominant categories: "
                        f"Usability, Service, Support, Others. "
                        f"Provide only the category name."
                )
                # print(classifier.response)
                sentiment = "Positive"
                if "Usability" in classifier.response:
                    comment_classification.append({
                        "sentiment":sentiment,
                        "classification": "Usability",
                        "user_review":comment,
                    })
                elif "Service" in classifier.response:
                    comment_classification.append({
                        "sentiment":sentiment,
                        "classification": "Service",
                        "user_review":comment,
                    })
                elif "Support" in classifier.response:
                    comment_classification.append({
                        "sentiment":sentiment,
                        "classification": "Support",
                        "user_review":comment,
                    })
                else:
                    comment_classification.append({
                        "sentiment":sentiment,
                        "classification": "Others",
                        "user_review":comment,
                    })
            if comment_classification:
                df = pd.DataFrame(comment_classification)
                json_file_name = "reddit_positive_review_classification.json"
                df.to_json(json_file_name, index=False)
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
                    prompt=f"Classify the entire {comment} into one of the following dominant categories: "
                           f"Usability, Service, Support, Others. "
                           f"Provide only the category name."
                )
                sentiment = "Negative"
                if "Usability" in classifier.response:
                    comment_classification.append({
                        "sentiment": sentiment,
                        "classification": "Usability",
                        "user_review": comment,
                    })
                elif "Service" in classifier.response:
                    comment_classification.append({
                        "sentiment": sentiment,
                        "classification": "Service",
                        "user_review": comment,
                    })
                elif "Support" in classifier.response:
                    comment_classification.append({
                        "sentiment": sentiment,
                        "classification": "Support",
                        "user_review": comment,
                    })
                else:
                    comment_classification.append({
                        "sentiment": sentiment,
                        "classification": "Others",
                        "user_review": comment,
                    })
            if comment_classification:
                df = pd.DataFrame(comment_classification)
                json_file_name = "reddit_negative_review_classification.json"
                df.to_json(json_file_name, index=False)
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
                    prompt=f"Classify the entire {comment} into one of the following dominant categories: "
                           f"Usability, Service, Support, Others. "
                           f"Provide only the category name."
                )
                # print(classifier.response)
                sentiment = "Neutral"
                if "Usability" in classifier.response:
                    comment_classification.append({
                        "sentiment": sentiment,
                        "classification": "Usability",
                        "user_review": comment,
                    })
                elif "Service" in classifier.response:
                    comment_classification.append({
                        "sentiment": sentiment,
                        "classification": "Service",
                        "user_review": comment,
                    })
                elif "Support" in classifier.response:
                    comment_classification.append({
                        "sentiment": sentiment,
                        "classification": "Support",
                        "user_review": comment,
                    })
                else:
                    comment_classification.append({
                        "sentiment": sentiment,
                        "classification": "Others",
                        "user_review": comment,
                    })
            if comment_classification:
                df = pd.DataFrame(comment_classification)
                json_file_name = "reddit_neutral_review_classification.json"
                df.to_json(json_file_name, index=False)
            else:
                print(" No reviews found!")

        except Exception as e:
            print(f"Error fetching reviews: {e}")



