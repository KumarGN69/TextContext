import pandas as pd
import dotenv, os
from custom_llm import LLMModel

dotenv.load_dotenv()

model = LLMModel()
client = model.getclientinterface()

df = pd.read_csv("inputfile.csv", header=0, delimiter=",")
# print(df['Critical User Journey Problem area'])
# print(df['Component'])
# print(df['1P Devices  Combination'])

query = client.generate(
    model= os.getenv('INFERENCE_MODEL'),
    prompt = (
                f"You are an expert in writing up search queries on Reddit to extract maximum user reviews."
                f"Generate exhaustive set of meaningful and relevant search queries containing combination"
                f"of information in {df['1P Devices  Combination']} and {df['Critical User Journey Problem area']}"
                f" and {df['Component']} and {df['Feature/ Functionality']}"
                f"Output only those queries which include the information in {df['Critical User Journey Problem area']}"
                f"Output the queries as a list without any additional explanation or new lines."
                f"Exclude all NaN values. Output each query on new line"
                f"DO not include - in front of the query"
        )
)
search_queries = (query.response).splitlines()
queries = [] 
for search_query in search_queries:
    queries.append({
        "queries":search_query
    })
    print(search_query)

df = pd.DataFrame(queries)
df.to_json("./search_queries.json",index=False)
df.to_csv("./search_queries.csv", index=False)
