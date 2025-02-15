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
        df= pd.read_json("./reddit_positive_reviews.json")
        comment_list = [df['comment'][record] for record in range(0,df['comment'].size)]
        comment_classification =[]
        for comment in comment_list:
            classifier = self.client.generate(
                model=self.MODEL,
                prompt=f"Classify the entire {comment} into one of the following dominant categories: "
                    f"Functionality, Service, Support, Others. "
                    f"Provide only the category name."
            )
            # print(classifier.response)
            sentiment = "Positive"
            if "Functionality" in classifier.response:
                comment_classification.append({
                    "sentiment":sentiment,
                    "classfication": "Functionality",
                    "user_review":comment,
                })
            elif "Service" in classifier.response:
                comment_classification.append({
                    "sentiment":sentiment,
                    "classfication": "Service",
                    "user_review":comment,
                })
            elif "Support" in classifier.response:
                comment_classification.append({
                    "sentiment":sentiment,
                    "classfication": "Support",
                    "user_review":comment,
                })
            else:
                comment_classification.append({
                    "sentiment":sentiment,
                    "classfication": "Others",
                    "user_review":comment,
                })

        # create csv and json files for neutral comments
        if comment_classification:
            df = pd.DataFrame(comment_classification)
            csv_file_name = "reddit_positive_review_classification.csv"
            json_file_name = "reddit_positive_review_classification.json"
            df.to_csv(csv_file_name, index=False)
            df.to_json(json_file_name, index=False)
            print(f"\n Data saved files successfully '")
        else:
            print(" No reviews found!")


    def classifyNegativeReviews(self):
        df= pd.read_json("./reddit_negative_reviews.json")
        comment_list = [df['comment'][record] for record in range(0,df['comment'].size)]
        comment_classification =[]
        for comment in comment_list:
            classifier = self.client.generate(
                model=self.MODEL,
                prompt=f"Classify the entire {comment} into one of the following dominant categories: "
                    f"Functionality, Service, Support, Others. "
                    f"Provide only the category name."
            )
            # print(classifier.response)
            sentiment = "Negative"
            if "Functionality" in classifier.response:
                comment_classification.append({
                    "sentiment":sentiment,
                    "classfication": "Functionality",
                    "user_review":comment,
                })
            elif "Service" in classifier.response:
                comment_classification.append({
                    "sentiment":sentiment,
                    "classfication": "Service",
                    "user_review":comment,
                })
            elif "Support" in classifier.response:
                comment_classification.append({
                    "sentiment":sentiment,
                    "classfication": "Support",
                    "user_review":comment,
                })
            else:
                comment_classification.append({
                    "sentiment":sentiment,
                    "classfication": "Others",
                    "user_review":comment,
                })

        # create csv and json files for neutral comments
        if comment_classification:
            df = pd.DataFrame(comment_classification)
            csv_file_name = "reddit_negative_review_classification.csv"
            json_file_name = "reddit_negative_review_classification.json"
            df.to_csv(csv_file_name, index=False)
            df.to_json(json_file_name, index=False)
            print(f"\n Data saved files successfully '")
        else:
            print(" No reviews found!")


    def classifyNeutralReviews(self):
        df= pd.read_json("./reddit_neutral_reviews.json")
        comment_list = [df['comment'][record] for record in range(0,df['comment'].size)]
        comment_classification =[]
        for comment in comment_list:
            classifier = self.client.generate(
                model=self.MODEL,
                prompt=f"Classify the entire {comment} into one of the following dominant categories: "
                    f"Functionality, Service, Support, Others. "
                    f"Provide only the category name."
            )
            # print(classifier.response)
            sentiment = "Neutral"
            if "Functionality" in classifier.response:
                comment_classification.append({
                    "sentiment":sentiment,
                    "classfication": "Functionality",
                    "user_review":comment,
                })
            elif "Service" in classifier.response:
                comment_classification.append({
                    "sentiment":sentiment,
                    "classfication": "Service",
                    "user_review":comment,
                })
            elif "Support" in classifier.response:
                comment_classification.append({
                    "sentiment":sentiment,
                    "classfication": "Support",
                    "user_review":comment,
                })
            else:
                comment_classification.append({
                    "sentiment":sentiment,
                    "classfication": "Others",
                    "user_review":comment,
                })

        # create csv and json files for neutral comments
        if comment_classification:
            df = pd.DataFrame(comment_classification)
            csv_file_name = "reddit_neutral_review_classification.csv"
            json_file_name = "reddit_neutral_review_classification.json"
            df.to_csv(csv_file_name, index=False)
            df.to_json(json_file_name, index=False)
            print(f"\n Data saved files successfully '")
        else:
            print(" No reviews found!")

