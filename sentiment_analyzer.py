import json
import pandas as pd
from textblob import TextBlob


class SentimentAnalyzer():
    """

    """
    def __init__(self):
        self.positive_sentiments = 0
        self.negative_sentiments = 0
        self.neutral_sentiments = 0
        self.unclassified_sentiments = 0
        self.negative_comments = []
        self.neutral_comments = []
        self.positive_comments = []
        self.unclassified_comments = []
    def assessSentiments(self, reviews: list):
        """

        """
        for review in reviews:
            user_review = f"{review['user_review']['post_title']}+{review['user_review']['self_text']}"
            # user_review = f"{review['post_title']}+{review['self_text']}"
            sentiment = TextBlob(user_review).sentiment
            if sentiment.subjectivity <= 0.65 and sentiment.polarity > 0.05:
                self.positive_sentiments += 1
                self.positive_comments.append(
                    {
                        "sentiment": "Positive",
                        "user_review": user_review
                    }
                )
                # print(self.positive_comments)
            elif sentiment.subjectivity <= 0.65 and sentiment.polarity < -0.05:
                self.negative_sentiments += 1
                self.negative_comments.append(
                    {
                        "sentiment": "Negative",
                        "user_review": user_review
                    }
                )
                # print(self.neutral_sentiments)
            elif sentiment.subjectivity <= 0.65 and (sentiment.polarity >= -0.05 and sentiment.polarity <= 0.05):
                self.neutral_sentiments += 1
                self.neutral_comments.append(
                    {
                        "sentiment": "Neutral",
                        "user_review": user_review
                    }
                )
                # print(self.neutral_sentiments)
            else:
                self.unclassified_sentiments += 1
                self.unclassified_comments.append(
                    {
                        "sentiment": "Unclassified",
                        "user_review": user_review
                    }
                )
                print(f"Subjectivity of unclassified review: {sentiment.subjectivity}")
        self.saveSentimentsToFile()
        
    def saveSentimentsToFile(self):
        """

        """
        if self.positive_sentiments:
            try:
                df = pd.DataFrame(self.positive_comments)
                df.to_json("reddit_positive_reviews.json")
                df.to_csv("reddit_positive_reviews.csv")
            except Exception as e:
                print(f"Error fetching positive reviews: {e}")
        else:
            print("No positive reviews found!")

    # create json files for negative reviews with classification
        if self.negative_sentiments:
            try:
                df = pd.DataFrame(self.negative_comments)
                df.to_json("reddit_negative_reviews.json")
                df.to_csv("reddit_negative_reviews.csv")
            except Exception as e:
                print(f"Error fetching negative reviews: {e}")
        else:
            print("No negative reviews found!")
        
        # create json files for neutral reviews with classification
        if self.neutral_sentiments:
            try:
                df = pd.DataFrame(self.neutral_comments)
                df.to_json("reddit_neutral_reviews.json")
                df.to_csv("reddit_neutral_reviews.csv")
            except Exception as e:
                print(f"Error fetching neutral reviews: {e}")
        else:
            print("No neutral reviews found!")

        # create json files for unclassified reviews
        if self.unclassified_sentiments:
            try:
                df = pd.DataFrame(self.unclassified_comments)
                df.to_json("reddit_unclassified_reviews.json")
                df.to_csv("reddit_unclassified_reviews.csv")
            except Exception as e:
                print(f"Error fetching unclassified reviews: {e}")
        else:
            print("No unclassified reviews found!")
