import json
from textblob import TextBlob

from reddit_handler import RedditHandler
from sentiment_analyzer import SentimentAnalyzer

if __name__ == "__main__":
    reddit = RedditHandler()
    reviews= json.loads(json.dumps(reddit.fetch_reviews()))

    sentiments = SentimentAnalyzer()
    sentiments.assessSentiments(reviews=reviews)

    print(f"Positive: {sentiments.positive_sentiments}, Negative:{sentiments.negative_sentiments}, Nuetral: {sentiments.nuetral_sentiments}")
    for comment in sentiments.negative_comments:
        print(comment)