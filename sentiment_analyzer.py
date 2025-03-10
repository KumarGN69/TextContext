import json
import pandas as pd
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from pandas import DataFrame


class SentimentAnalyzer():
    """

    """

    def __init__(self):
        """
            Class for assessing the sentiments for set of extracted reviews
            uses vader sentiment analyzer
        """
        self.positive_sentiments = 0
        self.negative_sentiments = 0
        self.neutral_sentiments = 0
        self.unclassified_sentiments = 0
        self.negative_comments = []
        self.neutral_comments = []
        self.positive_comments = []
        self.unclassified_comments = []
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def assessSentiments(self, reviews):
        """

        :param reviews: Extracted reviews , read from saved file
        :return: None.
        :Saves the sentiments to different csv and json files, positive, negative, neutral and unclassfied
        """
        user_reviews = [f"{reviews['post_title'][record]}.{reviews['self_text'][record]}" for record in range(0,reviews['post_title'].size)]

        for user_review in user_reviews:
            sentiment_score = self.sentiment_analyzer.polarity_scores(user_review)['compound']
            if sentiment_score >= 0.05:
                self.positive_sentiments += 1
                self.positive_comments.append(
                    {
                        "sentiment": "Positive",
                        "user_review": user_review
                    }
                )
                # print(self.positive_comments)
            elif sentiment_score <= -0.05:
                self.negative_sentiments += 1
                self.negative_comments.append(
                    {
                        "sentiment": "Negative",
                        "user_review": user_review
                    }
                )
                # print(self.neutral_sentiments)
            elif sentiment_score >-0.05 and sentiment_score < 0.05:
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
            #     print(f"Subjectivity of unclassified review: {sentiment.subjectivity}")
        self.saveSentimentsToFile()

    def saveSentimentsToFile(self):
        """
        Saves the assessed sentiments to separate csv, json files for positive, negative, neutral and unclassfied
        :return: None
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
