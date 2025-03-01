from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from gensim import corpora, models
import nltk

nltk.download("punkt_tab")
nltk.download("stopwords")

# Preprocessing
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    return [word for word in tokens if word.isalnum() and word not in stop_words]

# Sample text corpus
corpus = [
    "Google Pixel phones have excellent AI-powered cameras.",
    "Pixel Buds provide great sound quality and noise cancellation.",
    "Pixel Watch integrates well with the Google ecosystem.",
    "The Android experience on Pixel devices is very smooth."
]

# Tokenize and preprocess text
processed_corpus = [preprocess_text(doc) for doc in corpus]

# Create dictionary and bag-of-words model
dictionary = corpora.Dictionary(processed_corpus)
bow_corpus = [dictionary.doc2bow(doc) for doc in processed_corpus]

# Train LDA model
lda_model = models.LdaModel(bow_corpus, num_topics=2, id2word=dictionary, passes=10)

# Print key themes
for idx, topic in lda_model.print_topics(-1):
    print(f"🔹 Topic {idx+1}: {topic}")
