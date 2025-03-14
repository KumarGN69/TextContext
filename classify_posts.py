import csv, time, warnings
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

#----------------------------------------------------------------------------------------
# instantiate a text generator, classifier , summarizer and sentiment analyzer
generator = pipeline(
            task="text-generation",
            model="google/gemma-2-9b-it",
            top_k=1,
            device=-1,
        )

classifier = pipeline(
            task="zero-shot-classification",
            model="MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli",
            top_k=1,
            temparature=0.1,
            max_length=512,
            truncation=True,
            device=-1,
        )

summarizer = pipeline(
            task="summarization",
            model="facebook/bart-large-cnn",
            top_k=1,

            device=-1,
        )

analyzer = SentimentIntensityAnalyzer()
#----------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------
class ProcessReview:
    """

    """
    def __init__(self):
        warnings.filterwarnings("ignore")

    #----------------------------------------------------------------------------------------
    # define methods for classification, sentiment analysis, summarization and test cuj generation

    def classify_review(self, review:str):
        """
        classifies the reviews into categories based on the labels
        :param
            review: user_review
            labels: list of labels
        :return: classification of the user review
        """
        # labels for classification
        labels = ["Audio", "Voice", "Call drop", "Car Kit", "Bluetooth", "Wifi", "Other"]

        classify_prompt = f"classify the review strictly into the label which has the max score"
        classification = classifier(review, prompt= classify_prompt, candidate_labels=labels, multi_label=False)
        category = classification['labels']
        max_score_index = classification['scores'].index(max(classification['scores']))
        return category[max_score_index]


    #----------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------
    def summarize_review(self, review:str):
        """
        classifies the reviews into categories based on the labels
        :param
            review: user_review
            labels: list of labels
        :return: classification of the user review
        """

        summary_prompt = (f"You are an expert in summarization. Please condense the review into "
                          f"two concise and impactful sentences.")
        messages = [
            {
                "role": "user",
                "content": summary_prompt
            },
        ]
        summary = summarizer(messages)
        return summary[0]["generated_text"][-1]["content"].strip()


    #----------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------
    def generate_testcuj(self,review:str):
        """
        classifies the reviews into categories based on the labels
        :param
            review: user_review
            labels: list of labels
        :return: classification of the user review
        """

        testcuj_prompt = (f"Generate a detailed test user journey based on contents in the  {review}"
                          f"in concise langaue that is easy for tester to follow and implement")
        messages = [
            {
                "role": "user",
                "content": testcuj_prompt
            },
        ]
        testcuj = generator(messages)
        return testcuj[0]["generated_text"][-1]["content"].strip()


    #----------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------
    def analyze_sentiment(self, review:str):
        """
        assess the sentiments of the review into positive, negative, neutral and unclassified
        :param
            review: user review
        :return: sentiment text based on score
        """
        # create a sentiment analyzer

        score = analyzer.polarity_scores(review)['compound']
        if score >= 0.1:
            return "Positive"
        elif score <= - 0.1:
            return "Negative"
        else:
            return "Neutral"


    #----------------------------------------------------------------------------------------


    #----------------------------------------------------------------------------------------
    def updateSaveClassifications(self):
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
        posts['sentiment'] = posts['combined_reviews'].apply(self.analyze_sentiment)

        print(f"classifying into categories")
        posts['category'] = posts['combined_reviews'].apply(self.classify_review)

        # print(f"summarizing the reviews")
        # posts['summary'] = posts['combined_reviews'].apply(self.summarize_review)

        print(f"generating test cuj")
        posts['test_cuj'] = posts['combined_reviews'].apply(self.generate_testcuj)

        # print(posts['sentiment'],posts['category'],posts['combined_reviews'])
        print(posts.columns)
        if not posts.empty:
            json_filename = "classified_posts.json"
            csv_filename = "classified_posts.csv"
            posts.to_json(json_filename, index=False)
            posts.to_csv(csv_filename, index=False, quoting=csv.QUOTE_ALL, quotechar='"')
        end = time.time()
        print(f"time taken for sentiment and classification: {end - start}")


    #----------------------------------------------------------------------------------------


#----------------------------------------------------------------------------------------
if __name__ == "__main__":
    review_processor = ProcessReview()
    review_processor.updateSaveClassifications()
