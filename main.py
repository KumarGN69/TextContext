import json, os, dotenv
import pandas as pd

from reddit_handler import RedditHandler
from sentiment_analyzer import SentimentAnalyzer
from review_classification import ReviewClassifier

if __name__ == "__main__":
    dotenv.load_dotenv()
    # Create reddit handler and fetch reddit posts based on a specific string
    reddit = RedditHandler(query=os.getenv('SEARCH_QUERY'))
    reviews= json.loads(json.dumps(reddit.fetch_reviews()))

    # analyze sentiments of the retrieved posts 
    sentiments = SentimentAnalyzer()
    print(f"Assessment of extracted sentiments in progress")
    sentiments.assessSentiments(reviews=reviews)
    print(f"Sentiment assessment summary: ")
    # print the sentiment analysis summary
    print(f"Positive: {sentiments.positive_sentiments}, Negative:{sentiments.negative_sentiments}, Neutral: {sentiments.neutral_sentiments}")

    print(f"Starting classification of reviews into different categories")
    # create json files for positive reviews with classification
    classifier = ReviewClassifier()
    for sentiment in ["positive","negative","neutral"]:
        classifier.classifyReviews(sentiment=sentiment)
        




