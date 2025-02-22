from review_classification import ReviewClassifier
import pandas as pd
import multiprocessing

num_workers = multiprocessing.cpu_count()
print(num_workers)

df = pd.read_json(f"./reddit_negative_reviews.json")
queries = [df['user_review'][record] for record in range(0, df['user_review'].size)]

classifier = ReviewClassifier()
def classify_reviews(reviews: list):
    return classifier.classifyAndUpdate(sentiment="negative", comment_list=reviews)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    with multiprocessing.Pool(processes=1) as pool:
        results = pool.map(classify_reviews, queries)
        print(results)
