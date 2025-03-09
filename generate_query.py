import pandas as pd
import dotenv, os
from custom_llm import LLMModel


class GenerateSearchQueries:

    def __init__(self):
        dotenv.load_dotenv()
        self.model = LLMModel()
        self.client = self.model.getclientinterface()

    def generateQueries(self):
        df = pd.read_csv("inputfile.csv", header=0, delimiter=",")
        # print(df['Critical User Journey Problem area'])
        # print(df['Component'])
        # print(df['1P Devices  Combination'])
        query = self.client.generate(
            model=self.model.MODEL_NAME,
            # prompt=(
            #     f"You are an expert in writing up search queries on Reddit to extract maximum user reviews."
            #     f"Generate exhaustive set of relevant search queries in meaningful sentences based on combination"
            #     f"of information in {df['1P Devices  Combination']} and {df['Critical User Journey Problem area']}"
            #     f"and {df['Component']} and {df['Feature/ Functionality']}"
            #     f"Do not include queries which do not have information in {df['Critical User Journey Problem area']}"
            #     f"Output the queries as a list without any additional explanation or new lines."
            #     f"Exclude all NaN values. Output each query on new line"
            #     f"DO not include - in front of the query"
            # )
            prompt = (
                f"You are an expert in crafting targeted Reddit search queries to extract comprehensive user feedback. "
                f"Generate a complete list of natural-language search phrases that combine these elements from our "
                f"dataset:"
                f"1. **Device Combinations** (from {df['1P Devices  Combination']})"
                f"2. **Core User Pain Points** (from {df['Critical User Journey Problem area']}, REQUIRED)"
                f"3. **Hardware/Software Components** (from {df['Component']})"
                f"4. **Key Features** (from {df['Feature/ Functionality']})"
                
                f"**Requirements:**"
                f"- Mandatory inclusion of Critical User Journey Problem area"
                f"- Exclude any entry with missing values (NaNs) in ANY field"
                f"- Create 20-30 word natural phrases, not keyword lists"
                f"- Blend elements contextually (e.g., '[Device] [Problem] during [Feature] usage due to [Component]')"
                f"- Output as clean text with one query per line"
                f"- No markdown, numbering, or special characters"
                
                f"Example structure:"
                f"Troubleshooting [Device Combination] [Problem Area] caused by [Component] failures during [Feature] "
                f"operation"

        )
    )
        search_queries = (query.response).splitlines()
        queries = []
        for search_query in search_queries:
            queries.append({
                "queries": search_query
            })
            # print(search_query)

        df = pd.DataFrame(queries)
        df.to_json("./search_queries.json", index=False)
        df.to_csv("./search_queries.csv", index=False)
