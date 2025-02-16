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
    if sentiments.positive_sentiments:
        try:
            df = pd.DataFrame(sentiments.positive_comments)
            df.to_json("reddit_positive_reviews.json")
            classifier.classifyPositiveReviews()
        except Exception as e:
            print(f"Error fetching positive reviews: {e}")
    else:
        print("No positive reviews found!")

    # create json files for negative reviews with classification
    if sentiments.negative_sentiments:
        try:
            df = pd.DataFrame(sentiments.negative_comments)
            df.to_json("reddit_negative_reviews.json")
            classifier.classifyNegativeReviews()
        except Exception as e:
            print(f"Error fetching negative reviews: {e}")
    else:
        print("No negative reviews found!")
    
    # create json files for neutral reviews with classification
    if sentiments.neutral_sentiments:
        try:
            df = pd.DataFrame(sentiments.neutral_comments)
            df.to_json("reddit_neutral_reviews.json")
            classifier.classifyNeutralReviews()
        except Exception as e:
            print(f"Error fetching neutral reviews: {e}")
    else:
        print("No neutral reviews found!")
    




