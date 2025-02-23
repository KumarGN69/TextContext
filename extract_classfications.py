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

df = pd.read_json(f"./reddit_negative_reviews.json")
queries = [df['user_review'][record] for record in range(0, df['user_review'].size)]

classifier = ReviewClassifier()

def classify_reviews(review: str):
    return classifier.classifyReview(sentiment="negative", comment=review)




if __name__ == "__main__":
    multiprocessing.freeze_support()
    # with multiprocessing.Pool(processes=1) as pool:
    #     results = pool.map(classify_reviews, queries)
    #     print(results)

 

    # # # Dummy classification function
    # # def classify_text(text):
    # #     return f"Processed: {text}"

    # # List of texts to classify
    # texts = ["text1", "text2", "text3", "text4", "text5", "text6"]

    # Use Dask `delayed` to create lazy computations
    client = Client(n_workers=num_workers,processes=True,threads_per_worker=1)  # Adjust workers based on CPU cores
    print(client)
    tasks = [delayed(classify_reviews)(review=query) for query in queries]

    # Execute in parallel
    results = compute(*tasks)
   
    # print(results)
    classifier.saveToFile(sentiment="negative",comment_classification=results)
    client.close()



