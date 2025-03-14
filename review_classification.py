from custom_llm import LLMModel
import pandas as pd
import os, dotenv, csv
from pydantic import BaseModel


class Sentiment(BaseModel):
    sentiment: str


class Summary(BaseModel):
    summary: str


class TestCUJ(BaseModel):
    test_user_journey: str


class UserReview(BaseModel):
    user_review: str


class Category(BaseModel):
    category: str


class Output(BaseModel):
    sentiment: Sentiment
    category: Category
    user_review: UserReview
    summary: Summary
    test_user_journey: TestCUJ


class ReviewClassifier:
    """

    """

    def __init__(self):
        dotenv.load_dotenv()
        self.model = LLMModel()
        # self.client = self.model.getclientinterface()
        self.MODEL = os.getenv('INFERENCE_MODEL')
        self.classifiers = {"Audio", "Voice Quality", "Bluetooth", "Wi-Fi", "Call drop", "Car Kit", "Other"}
        # self.classifiers = {
        #     "Audio Issues": ["audio", "sound"],
        #     "Video Issues": ["video", "display"],
        #     "User Experience": ["experience", "user"],
        #     "Service": ["service", "support"],
        #     "Support": ["support", "help"],
        #     "Others": ["other"],
        #     "Technical": ["technical", "tech"],
        #     "Voice Quality": ["voice", "call quality"],
        #     "Bluetooth": ["bluetooth"],
        #     "WiFi": ["wifi", "wireless"],
        #     "Call drop": ["call drop", "dropped call"]
        # }
        self.task = (f"You are an expert in assessing sentiment, classifying the review into a set of predefined labels"
                     f"and summarizing the review into a crisp two sentences and generating step wise test user journey ")
        self.output_criteria = (f"Return only category names from {self.classifiers} ensuring: "
                                f"1. No new lines or extra white spaces. "
                                f"2. No additional words, explanations, or qualifiers. "
                                f"3. Map only to the relevant categories from the provided categories: {self.classifiers} ."
                                f"4. Do not include all categories when no relevant mapping is detected.Use None")

        self.prompt = (
                        f"Use only the categories from {self.classifiers}. "
                        f"Strictly adhere to criteria in {self.output_criteria} for labeling "
                        f"Output Format: "
                        f"return the output in a structured JSON format as follows:\n"
                        f"{{\n"
                        f"    'sentiment': '',\n"
                        f"    'category': '',\n"
                        f"    'user_review': '',\n"
                        f"    'summary': '',\n"
                        f"    'test_user_journey': ''\n"
                        f"}}"
                        f"return only the sentiment, label for the category and do not append any other text to them"
                     )

    def classifyReviews(self, sentiment: str):
        """
        """
        try:
            df = pd.read_json(f"./reddit_{sentiment}_reviews.json")
            df = df.astype(str)
            comment_list = [df['user_review'][record] for record in range(0, df['user_review'].size)]
            print(f"Classification of {sentiment} reviews in progress")
            comment_classification = self.classifyAndUpdate(
                comment_list=comment_list,
                sentiment=sentiment
            )

            print(f"Classification of {sentiment} reviews complete ")
            if comment_classification:
                self.saveToFile(
                    sentiment=sentiment,
                    comment_classification=comment_classification
                )
            else:
                print(" No reviews found!")

        except Exception as e:
            print(f"Error fetching reviews: {e}")

    def classifyAndUpdate(self, comment_list: list, sentiment: str):
        """
        """
        classifications = []
        # print("Entering classification")
        for comment in comment_list:
            client = self.model.getclientinterface()
            # print("Classification started")
            classifier = client.generate(
                model=self.MODEL,
                prompt=f"Classify the {comment} adhering to guidelines in {self.prompt}"
            )
            sentiment = sentiment
            summarizer = client.generate(
                model=self.MODEL,
                prompt=(f"You are an expert in summarization. Please condense the following {comment} into "
                        f"two concise and impactful sentences.")
            )
            testCUJ = client.generate(
                model=self.MODEL,
                prompt=(f"You are a senior, experienced software quality analyst and tester specializing "
                        f"in mobile phones and accessories. Generate clear and concise instructions to create a "
                        f"test user journey that addresses the key issue described in the following {comment}, "
                        f"using language and descriptions that a tester can easily understand and follow")
            )
            # print("Classification done")
            classifications.append({
                "sentiment": sentiment,
                "categories": [classifier.response],
                "user_review": comment,
                "summary": [summarizer.response],
                "test_user_journey": [testCUJ.response]
            })
            # print("Updates done")
        return classifications

    def saveToFile(self, sentiment: str, comment_classification: list):
        """
        """
        print(comment_classification)
        df = pd.DataFrame(comment_classification)
        json_file_name = f"reddit_{sentiment}_review_classification.json"
        df.to_json(json_file_name,indent=4,orient="records")

        csv_file_name = f"reddit_{sentiment}_review_classification.csv"
        df.to_csv(csv_file_name, index=False, quoting=csv.QUOTE_ALL, quotechar='"')

    def classifyReview(self, comment: str, sentiment: str):
        """
        """
        classification = {}
        # print("Entering classification")
        # for comment in comment_list:
        model = LLMModel()
        client = model.getclientinterface()
        # print("Classification started")
        classifier = client.generate(
            model=self.MODEL,
            prompt=f"Classify the {comment} adhering to guidelines in {self.prompt}",
        )
        sentiment = sentiment
        # print("Classification done")
        summarizer = client.generate(
            model=self.MODEL,
            prompt=(f"You are an expert in summarization. Please condense the following {comment} into "
                    f"two concise and impactful sentences.")
        )
        testCUJ = client.generate(
            model=self.MODEL,
            prompt=(f"You are a senior, experienced software quality analyst and tester specializing "
                    f"in mobile phones and accessories. Generate clear and concise instructions to create a "
                    f"test user journey that addresses the key issue described in the following {comment},"
                    f"using language and descriptions that a tester can easily understand and follow")
        )
        classification = {
            "sentiment": sentiment,
            "categories": [classifier.response],
            "user_review": comment,
            "summary": [summarizer.response],
            "test_user_journey": [testCUJ.response]
        }
        # print("Updates done")
        return classification

    def processReview(self, comment: str, sentiment: str):
        """
        """
        classification = {}
        # print("Entering classification")
        # for comment in comment_list:
        model = LLMModel()
        client = model.getclientinterface()
        # print("Classification started")
        generated_content = client.generate(
            model=self.MODEL,
            prompt=f"Perform the task detailed in {self.task} on {comment} adhering to guidelines in {self.prompt}",
            format=Output.model_json_schema()
        )
        result = Output.model_validate_json(generated_content.response)
        # print(result)
        classification = {
            "sentiment": result.sentiment,
            "category": result.category,
            "user_review": comment,
            "summary": result.summary,
            "test_user_journey": result.test_user_journey
        }
        # print(classification)
        return classification
        # print(result.sentiment, result.categories,result.summary, result.test_user_journey)
        #
        # return generated_content
