import pandas as pd
from scripts.llm_service import LLMOllamaClient

client = LLMOllamaClient(model="gpt-oss:20b")

df = pd.read_csv("oasst2_processed.csv")

system_prompt = """
Your task is to respond to the user question in the same romanized language the query was asked in.
You should not translate the user query into any native language. Just respond to the query in the same romanized language.
"""

for query in df["Query"][4:5]:
    print("query:", query)

    prompt = f"""
Query:
{query}
"""

    result = client.generate(
        system_prompt=system_prompt,
        prompt=prompt,
    )

    print("Model Response:")
    print(result)