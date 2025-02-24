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
        self.negative_comments = []
        self.neutral_comments = []
        self.positive_comments = []

    def assessSentiments(self, reviews: list):
        """

        """
        for review in reviews:
            user_review = f"{review['user_review']['post_title']}+{review['user_review']['self_text']}"
            sentiment = TextBlob(review['user_review']['self_text']).sentiment
            if sentiment.subjectivity <= 0.5 and sentiment.polarity > 0.05:
                self.positive_sentiments += 1
                self.positive_comments.append({
                        "sentiment": "Positive",
                        "user_review": user_review
                })
            elif sentiment.subjectivity <= 0.5 and sentiment.polarity < -0.05:
                self.negative_sentiments += 1
                self.negative_comments.append({
                        "sentiment": "Negative",
                        "user_review": user_review
                })
            elif sentiment.subjectivity <= 0.5 and (sentiment.polarity > -0.05 and sentiment.polarity < 0.05):
                self.neutral_sentiments += 1
                self.neutral_comments.append({
                        "sentiment": "Neutral",
                        "user_review": user_review
                })
                
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
