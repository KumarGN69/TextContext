import json, csv, time
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# create a pipeline for classification
classifier = pipeline(
      task="zero-shot-classification",
      model="facebook/bart-large-mnli",
      top_k=1,
      temparature = 0.1
    )

# labels for classification
# labels = ["audio", "earbuds","earphones" "sound", "voice", "call quality", "bluetooth", "wifi", "wireless", "call drop", "dropped call", "other"]
labels = ["Audio", "Voice", "Call drop", "Bluetooth", "Wifi","Customer Service", "Support" "Other"]
# create a sentiment analyzer
analyzer = SentimentIntensityAnalyzer()


def classify_review(review):
    """
    classifies the reviews into categories based on the labels
    :param
        review: user_review
        labels: list of labels
    :return: classification of the user review
    """
    classification= classifier(review, candidate_labels=labels)
    category = classification['labels']
    max_score_index = classification['scores'].index(max(classification['scores']))
    if classification['scores'][max_score_index] > 0.75 :
        return category[max_score_index]
    else:
        return "Not Relevant"



def classify_sentiment(review):
    """
    assess the sentiments of the review into positive, negative, neutral and unclassified
    :param
        review: user review
    :return: sentiment text based on score
    """
    score = analyzer.polarity_scores(review)['compound']
    if score >= 0.1:
        return "Positive"
    elif score <= - 0.1:
        return "Negative"
    else:
        return "Neutral"


def updateSaveClassifications():
    """
    assess the sentiments and classifies the reviews into different categories
    saves the classified reviews into a csv and json files
    :return: none.
    """
    # read file and convert all contents to strings
    start = time.time()
    posts = pd.read_csv('./all_posts.csv')
    posts = posts.astype(str)
    #combine the post title and review text
    print(f"combining title and self text")
    posts['combined_reviews'] = posts['post_title'] + posts['self_text']
    print(f"assessing sentiments")
    posts['sentiment'] = posts['combined_reviews'].apply(classify_sentiment)
    print(f"classifying into categories")
    posts['category'] = posts['combined_reviews'].apply(classify_review)
    # print(posts['sentiment'],posts['category'],posts['combined_reviews'])
    print(posts.columns)
    if not posts.empty:
        json_filename = "classified_posts.json"
        csv_filename = "classified_posts.csv"
        posts.to_json(json_filename, index=False)
        posts.to_csv(csv_filename, index=False, quoting=csv.QUOTE_ALL, quotechar='"')
    end = time.time()
    print(f"time taken for sentiment and classification: {end - start}")

if __name__ == "__main__":

    updateSaveClassifications()
