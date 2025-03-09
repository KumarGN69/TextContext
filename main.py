import json, os, dotenv
import pandas as pd

import multiprocessing, time
import dask
from dask import delayed, compute
from dask.distributed import Client
import dask.bag as db

from reddit_handler import RedditHandler
from sentiment_analyzer import SentimentAnalyzer
from review_classification import ReviewClassifier

num_workers = multiprocessing.cpu_count()
print(num_workers)
#create a classifier instance
classifier = ReviewClassifier()

# function for parallel processing of classification tasks
def classify_reviews(review: str,sentiment: str):
    return classifier.classifyReview(sentiment=sentiment, comment=review)

if __name__ == "__main__":
    dotenv.load_dotenv()
    # # Create reddit handler and fetch reddit posts based on a specific string
    df= pd.read_csv(f"./search_queries.csv")
    queries = [df['queries'][record] for record in range(0,df['queries'].size)]
    # reddit = RedditHandler(query=os.getenv('SEARCH_QUERY'))
    reddit = RedditHandler(queries=queries)
    reviews= json.loads(json.dumps(reddit.fetch_reviews()))

    # # analyze sentiments of the retrieved posts 
    # sentiments = SentimentAnalyzer()
    # print(f"Assessment of extracted sentiments in progress")
    # sentiments.assessSentiments(reviews=reviews)
    # print(f"Sentiment assessment summary: ")
    # # print the sentiment analysis summary
    # print(f"Positive: {sentiments.positive_sentiments}, Negative:{sentiments.negative_sentiments}, Neutral: {sentiments.neutral_sentiments}")

    # print(f"Starting classification of reviews into different categories")
    # # create json files for positive reviews with classification
    # # classifier = ReviewClassifier()
    # multiprocessing.freeze_support()


    # # start the classification process
    # start = time.time()
    # for sentiment in ["positive","negative","neutral"]:
    #     # read the sentiment files
    #     df = pd.read_json(f"./reddit_{sentiment}_reviews.json")
    #     queries = [df['user_review'][record] for record in range(0, df['user_review'].size)]

    #     # Use Dask `delayed` to create lazy computations
    #     client = Client(n_workers=int(num_workers), processes=True,
    #                     threads_per_worker=2)  # Adjust workers based on CPU cores
    #     print(client)
    #     tasks = [delayed(classify_reviews)(review=query, sentiment=sentiment) for query in queries]

    #     # Execute in parallel
    #     results = compute(*tasks)

    #     # print(results)
    #     # save the classifications into csv and json files
    #     classifier.saveToFile(sentiment=sentiment, comment_classification=results)
    #     client.close()
    # end = time.time()

    # print(f"time elapsed :", end - start)
        




