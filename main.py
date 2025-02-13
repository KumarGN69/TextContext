import json
from textblob import TextBlob

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
    reviews= json.loads(json.dumps(reddit.fetch_reviews()))

    sentiments = SentimentAnalyzer()
    sentiments.assessSentiments(reviews=reviews)

    print(f"Positive: {sentiments.positive_sentiments}, Negative:{sentiments.negative_sentiments}, Nuetral: {sentiments.nuetral_sentiments}")
    # for comment in sentiments.negative_comments:
    #     print(comment)

# nltk.download("punkt_tab")
# nltk.download("stopwords")

# # Preprocessing
# def preprocess_text(text):
#     tokens = word_tokenize(text.lower())
#     stop_words = set(stopwords.words("english"))
#     return [word for word in tokens if word.isalnum() and word not in stop_words]

# # Sample text corpus
# # corpus = [
# #     "Google Pixel phones have excellent AI-powered cameras.",
# #     "Pixel Buds provide great sound quality and noise cancellation.",
# #     "Pixel Watch integrates well with the Google ecosystem.",
# #     "The Android experience on Pixel devices is very smooth."
# # ]
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

# Input text
# text = """The Google Pixel 8 Pro has an amazing AI-powered camera that captures stunning photos.
#           The battery life is decent, lasting a full day under moderate usage.
#           However, some users have reported issues with the fingerprint sensor.
#           Overall, the Pixel 8 Pro provides a great Android experience with regular updates."""

comments = sentiments.nuetral_comments
for comment in comments:
    # Parse and tokenize
    parser = PlaintextParser.from_string(comment, Tokenizer("english"))

    # Use LSA (Latent Semantic Analysis) Summarizer
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, 2)  # Extract 2 sentences

    # Print summary
    print("🔹 Summary:")
    for sentence in summary:
        print(sentence)
