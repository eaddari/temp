from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import pandas as pd
from microservices.transforming_pipeline.components.anonimization.utils.anonymization_prompt import SYSTEM_PROMPT_LOCALIZATION
from openai import AzureOpenAI
import dotenv
import re

parquet_path = "C:\\desktopnoonedrive\\docgenofficial\\AIDocGen\\docgen-unofficial-docgen-test_part_0.parquet"


dotenv.load_dotenv()


def chunk_df_rows(df, chunk_size):
    for i in range(0, len(df), chunk_size):
        indices = list(df.index[i:i + chunk_size])
        chunk = df.iloc[i:i + chunk_size]["content"].tolist()
        yield indices, chunk

class AnonimizatorLocalization:
    def __init__(self):
        self.azure_model_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.subscription_key =  os.getenv("AZURE_OPENAI_API_KEY")
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version =  os.getenv("AZURE_OPENAI_VERSION")
        self.SYSTEM_PROMPT_LOCALIZATION = SYSTEM_PROMPT_LOCALIZATION

    def process_chunk(self, indices, chunk):
        user_content = "Please process each item below separately and provide an answer for each:\n"
        for i, text in enumerate(chunk):
            user_content += f"{i + 1}. {text}\n"
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT_LOCALIZATION},
            {"role": "user", "content": user_content},
        ]
        client = AzureOpenAI(
            api_version=self.api_version,
            azure_endpoint=self.azure_endpoint,
            api_key=self.subscription_key,
        )
        response = client.chat.completions.create(
            model=self.azure_model_deployment,
            temperature=0,
            messages=messages,
        )
        answer = response.choices[0].message.content.strip()
        return indices, answer

    def get_coordinates(self, df, chunk_size: int = 10, max_workers: int = 8) -> dict:
        results = {}
        chunks = chunk_df_rows(df, chunk_size)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.process_chunk, indices, chunk) for indices, chunk in chunks]
            for future in as_completed(futures):
                indices, answer = future.result()
                for idx in indices:
                    if idx not in results:
                        results[idx] = []
                    results[idx].append(answer)
        return results


if __name__ == "__main__":

    df = pd.read_parquet(parquet_path)
    anonymizer = AnonimizatorLocalization()
    coordinates_raw = anonymizer.get_coordinates(df, chunk_size=20)
    print(coordinates_raw)



# usare wrapper per chiamare i servizi anziche usare direttamente openai