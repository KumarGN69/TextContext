import json
from textblob import TextBlob


class SentimentAnalyzer():

    def __init__(self):
        self.positive_sentiments = 0
        self.negative_sentiments = 0
        self.neutral_sentiments = 0
        self.negative_comments = []
        self.neutral_comments = []
        self.positive_comments = []

    def assessSentiments(self, reviews: list):
        for review in reviews:
            user_review = f"{review['post_title']}+{review['self_text']}"
            sentiment = TextBlob(review['self_text']).sentiment
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
