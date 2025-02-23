from review_classification import ReviewClassifier
import pandas as pd
import multiprocessing
import dask
from dask import delayed, compute
from dask.distributed import Client
import dask.bag as db

# Initialize Dask Client to manage parallel processing
num_workers = multiprocessing.cpu_count()
print(num_workers)

#read the sentiment files
df = pd.read_json(f"./reddit_negative_reviews.json")
queries = [df['user_review'][record] for record in range(0, df['user_review'].size)]

#create a classifier instance 
classifier = ReviewClassifier()

# function for parallel processing of classification tasks
def classify_reviews(review: str):
    return classifier.classifyReview(sentiment="negative", comment=review)

# main function for using dask based parallel processing
if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    # Use Dask `delayed` to create lazy computations
    client = Client(n_workers=int((num_workers)/4),processes=True,threads_per_worker=2)  # Adjust workers based on CPU cores
    print(client)
    tasks = [delayed(classify_reviews)(review=query) for query in queries]

    # Execute in parallel
    results = compute(*tasks)
   
    # print(results)
    classifier.saveToFile(sentiment="negative",comment_classification=results)
    client.close()



