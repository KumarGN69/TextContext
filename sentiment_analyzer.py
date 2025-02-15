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
            comment = f"{review['post_title']}+{review['self_text']}"
            sentiment = TextBlob(review['self_text']).sentiment
            if sentiment.subjectivity <= 0.5 and sentiment.polarity > 0.05:
                self.positive_sentiments += 1
                # self.positive_comments.append(f"{review['post_title']}+{review['self_text']}")
                self.positive_comments.append({
                    "sentiment": "Positive",
                    "comment": comment
                })
            elif sentiment.subjectivity <= 0.5 and sentiment.polarity < -0.05:
                self.negative_sentiments += 1
                # self.negative_comments.append(f"{review['post_title']}+{review['self_text']}")
                self.negative_comments.append({
                    "sentiment": "Negative",
                    "comment": comment
                })
            elif sentiment.subjectivity <= 0.5 and (sentiment.polarity >= -0.05 and sentiment.polarity <= 0.05):
                self.neutral_sentiments += 1
                # self.neutral_comments.append(f"{review['post_title']}+{review['self_text']}")
                self.negative_comments.append({
                    "sentiment": "Neutral",
                    "comment": comment
                })
