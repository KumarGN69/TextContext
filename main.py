import json
from textblob import TextBlob
import pandas as pd

from reddit_handler import RedditHandler
from sentiment_analyzer import SentimentAnalyzer

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim import corpora, models
import nltk

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

if __name__ == "__main__":
    reddit = RedditHandler()
    # print(reddit.fetch_reviews())
    reviews= json.loads(json.dumps(reddit.fetch_reviews()))
    # print(reviews)
    sentiments = SentimentAnalyzer()
    sentiments.assessSentiments(reviews=reviews)
    print(f"Positive: {sentiments.positive_sentiments}, Negative:{sentiments.negative_sentiments}, Nuetral: {sentiments.neutral_sentiments}")
    # for sentiment in sentiments.positive_comments:
    #     print(f"neutral:{sentiment}")
    # print(f"Positive: {sentiments.positive_sentiments}, Negative:{sentiments.negative_sentiments}, Nuetral: {sentiments.neutral_sentiments}")
    # for comment in sentiments.negative_comments:
    #     print(comment)

    # nltk.download("punkt_tab")
    # nltk.download("stopwords")

    # # Preprocessing
    # def preprocess_text(text):
    #     tokens = word_tokenize(text.lower())
    #     stop_words = set(stopwords.words("english"))
    #     return [word for word in tokens if word.isalnum() and word not in stop_words]

    # corpus = sentiments.negative_comments
    # # Tokenize and preprocess text
    # processed_corpus = [preprocess_text(doc) for doc in corpus]

    # # Create dictionary and bag-of-words model
    # dictionary = corpora.Dictionary(processed_corpus)
    # bow_corpus = [dictionary.doc2bow(doc) for doc in processed_corpus]

    # # Train LDA model
    # lda_model = models.LdaModel(bow_corpus, num_topics=5, id2word=dictionary, passes=10)

    # # Print key themes
    # for idx, topic in lda_model.print_topics(-1):
    #     print(f"🔹 Topic {idx+1}: {topic}")

    # comments = sentiments.neutral_comments
    #
    # for comment in comments:
    #     # print(comment)
    #     # Parse and tokenize
    #     parser = PlaintextParser.from_string(comment, Tokenizer("english"))
    #
    #     # Use LSA (Latent Semantic Analysis) Summarizer
    #     summarizer = LsaSummarizer()
    #     summary = summarizer(parser.document, 2)  # Extract 2 sentences
    #
    #     # Print summary
    #     print("🔹 Summary:")
    #     for sentence in summary:
    #         # pass
    #         print(sentence)
    # reviewssentiment = [f"{review['post_title']}.{review['self_text']}" for review in reviews]
    if sentiments.positive_comments:
        df = pd.DataFrame(sentiments.positive_comments)
        file_name = "reddit_pixel_reviews.csv"
        df.to_csv(file_name, index=False)
        df.to_json("reddit_pixel_reviews.json")
        print(f"\n✅ Data saved successfully to '{file_name}'")
    else:
        print("⚠️ No reviews found!")