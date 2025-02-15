import json, os, dotenv
from textblob import TextBlob
import pandas as pd

from reddit_handler import RedditHandler
from sentiment_analyzer import SentimentAnalyzer
from review_classification import ReviewClassifier

# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from gensim import corpora, models
# import nltk

# from sumy.parsers.plaintext import PlaintextParser
# from sumy.nlp.tokenizers import Tokenizer
# from sumy.summarizers.lsa import LsaSummarizer


if __name__ == "__main__":
    dotenv.load_dotenv()
    # Create reddit handler and fetch reddit posts based on a specific string
    reddit = RedditHandler(query=os.getenv('SEARCH_QUERY'))
    reviews= json.loads(json.dumps(reddit.fetch_reviews()))
    
    # analyze sentiments of the retrieved posts 
    sentiments = SentimentAnalyzer()
    sentiments.assessSentiments(reviews=reviews)
    
    #print the sentiment analysis summary
    print(f"Positive: {sentiments.positive_sentiments}, Negative:{sentiments.negative_sentiments}, Nuetral: {sentiments.neutral_sentiments}")
    
    # create csv and json files for positive comments
    if sentiments.positive_comments:
        df = pd.DataFrame(sentiments.positive_comments)
        file_name = "reddit_positive_reviews.csv"
        df.to_csv(file_name, index=False)
        df.to_json("reddit_positive_reviews.json")
        print(f"\n Data saved successfully to '{file_name}'")
    else:
        print("No reviews found!")

    # create csv and json files for negative comments
    if sentiments.negative_comments:
        df = pd.DataFrame(sentiments.negative_comments)
        file_name = "reddit_negative_reviews.csv"
        df.to_csv(file_name, index=False)
        df.to_json("reddit_negative_reviews.json")
        print(f"\n Data saved successfully to '{file_name}'")
    else:
        print("No reviews found!")
    
    # create csv and json files for neutral comments
    if sentiments.neutral_comments:
        df = pd.DataFrame(sentiments.neutral_comments)
        file_name = "reddit_neutral_reviews.csv"
        df.to_csv(file_name, index=False)
        df.to_json("reddit_neutral_reviews.json")
        print(f"\n Data saved successfully to '{file_name}'")
    else:
        print(" No reviews found!")
    
    classifier = ReviewClassifier()
    classifier.classifyPositiveReviews()
    classifier.classifyNegativeReviews()
    classifier.classifyNeutralReviews()

    df= pd.read_json("./reddit_positive_review_classification.json")
    print(df)
    df= pd.read_json("./reddit_negative_review_classification.json")
    print(df)
    df= pd.read_json("./reddit_neutral_review_classification.json")
    print(df)

