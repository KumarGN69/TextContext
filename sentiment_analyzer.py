import json
from textblob import TextBlob

class SentimentAnalyzer():

    def __init__(self):
        self.positive_sentiments = 0
        self.negative_sentiments = 0
        self.nuetral_sentiments = 0
        self.negative_comments = []
        self.nuetral_comments = []
        self.positive_comments = []
    def assessSentiments(self, reviews:list):
        for review in reviews:
            sentiment = TextBlob(review['comment']).sentiment
            if sentiment.subjectivity <=0.5 and sentiment.polarity > 0.05: 
                self.positive_sentiments += 1
                self.positive_comments.append(review['comment'])
            elif sentiment.subjectivity <= 0.5 and sentiment.polarity < -0.05:
                self.negative_sentiments += 1
                self.negative_comments.append(review['comment'])
            elif sentiment.subjectivity <= 0.5 and (sentiment.polarity >= -0.05 and sentiment.polarity <= 0.05):
                self.nuetral_sentiments += 1
                self.nuetral_comments.append(review['comment'])