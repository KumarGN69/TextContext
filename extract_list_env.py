import pandas as pd
import dotenv, os
from custom_llm import LLMModel

dotenv.load_dotenv()

model = LLMModel()
client = model.getclientinterface()

df = pd.read_csv("./inputfile.txt",header=0,delimiter=",")

query = client.generate(
    model= os.getenv('INFERENCE_MODEL'),
    prompt = (
                f"You are an expert in writing up search queries on Reddit to extract maximum user reviews."
                f"Generate an exhaustive set of meaningful and relevant search queries as possible using"
                f"combinations of information in all columns of {df} for extracting relevant user reviews."
                f"Include all key words in a meaningful way."
                f"from Reddit. Output only the queries as a list without any additional explanation or new lines."
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

df = pd.DataFrame(queries)
df.to_json("./search_queries.json",index=False)
df.to_csv("./search_queries.csv", index=False)
