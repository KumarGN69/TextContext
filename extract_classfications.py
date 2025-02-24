from review_classification import ReviewClassifier
import pandas as pd
import multiprocessing, time
import dask
from dask import delayed, compute
from dask.distributed import Client
import dask.bag as db

# Initialize Dask Client to manage parallel processing
num_workers = multiprocessing.cpu_count()
print(num_workers)

#read the sentiment files
# df = pd.read_json(f"./reddit_negative_reviews.json")
# queries = [df['user_review'][record] for record in range(0, df['user_review'].size)]

#create a classifier instance 
classifier = ReviewClassifier()

# function for parallel processing of classification tasks
def classify_reviews(review: str):
    return classifier.classifyReview(sentiment="negative", comment=review)

# main function for using dask based parallel processing
if __name__ == "__main__":

    multiprocessing.freeze_support()

    # start the classification process
    start = time.time()

    # loop through all sentiment files
    for sentiment in ["positive"]:
        # read the sentiment files
        df = pd.read_json(f"./reddit_{sentiment}_reviews.json")
        queries = [df['user_review'][record] for record in range(0, df['user_review'].size)]

        # Use Dask `delayed` to create lazy computations
        client = Client(n_workers=int(num_workers),processes=True,threads_per_worker=2)  # Adjust workers based on CPU cores
        print(client)
        tasks = [delayed(classify_reviews)(review=query) for query in queries]

        # Execute in parallel
        results = compute(*tasks)

        # print(results)
        # save the classifications into csv and json files
        classifier.saveToFile(sentiment=sentiment,comment_classification=results)
        client.close()
    end = time.time()

    print(f"time elapsed :", end-start)



