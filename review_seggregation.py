from custom_llm import LLMModel
import pandas as pd

model = LLMModel()
client = model.getclientinterface()

df= pd.read_json("./reddit_pixel_reviews.json")
# print(df['post_title'])
comment_list = [df['comment'][record] for record in range(0,df['comment'].size)]
for comment in comment_list:
    category = client.generate(
        model="llama3.2",
        prompt=f"Classify the entire {comment} into one of the following dominant categories: "
               f"Functionality, Service, Support, Others. "
               f"Provide only the category name."
    )
    print(category.response)
