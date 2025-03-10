import json
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
def classify_vader(review):
    score = analyzer.polarity_scores(review)['compound']
    if score >= 0.05:
        return "Positive"
    elif score <=- 0.05:
        return "Negative"
    else:
        return "Neutral"
if __name__ == "__main__":
    posts = pd.read_csv('./all_posts.csv')

    posts['sentiment'] = (posts['post_title'] + posts['self_text']).apply(classify_vader)
    print(posts['post_title'], posts['self_text'], posts['sentiment'])