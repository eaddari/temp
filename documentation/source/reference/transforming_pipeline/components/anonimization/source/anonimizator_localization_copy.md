# microservices.transforming_pipeline.components.anonimization.source.anonimizator_localization_copy

Source file: `microservices\transforming_pipeline\components\anonimization\source\anonimizator_localization_copy.py`

## Source Code

```python
import os
import re
from components.anonimization.utils.anonymization_prompt import SYSTEM_PROMPT_LOCALIZATION
from components.anonimization.utils.chunk_df import chunk_dataframe
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

class AnonimizatorLocalization:

    def __init__(self):
        self.azure_model_deployment = os.getenv("OPENAI_API_DEPLOYMENT_NAME")
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.api_base = os.getenv("OPENAI_API_BASE")
        self.api_version = os.getenv("OPENAI_API_VERSION")
        self.SYSTEM_PROMPT_LOCALIZATION = SYSTEM_PROMPT_LOCALIZATION

        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.api_base
        )

    def process_whole_file_azure(self, df):
        items = "\n".join(f"[ROW {i}]: {text}" for i, text in enumerate(df["content"].tolist()))
        prompt = self.SYSTEM_PROMPT_LOCALIZATION + "\n" + items
        response = self.client.chat.completions.create(
            model=self.azure_model_deployment,
            messages=[{"role": "user", "content": prompt}]
        )
        return response
    
    def run_anonimizer_in_chunks(self, df, chunk_size=10):
            """
            Process the DataFrame in chunks to avoid token rate limits.
            Chunk size is the number of rows to process at once.
            Chunk size n = n rows of content.
            """
            all_coordinates = []
            for chunk in chunk_dataframe(df, chunk_size):
                response = self.process_whole_file_azure(chunk)
                content = response.choices[0].message.content
                result_lines = content.split("\n")
                all_coordinates.extend(result_lines[:len(chunk)])
            df['coordinates'] = all_coordinates[:len(df)]
            return df

    def censor_content(self, df, content_col='content', coords_col='coordinates', censor_tag='*****'):
        def censor_row(row):
            text = row[content_col]
            coords = row[coords_col]
            if isinstance(coords, str):
                matches = re.findall(r'\[(\d+):(\d+)\]', coords)
                coords = [(int(start), int(end)) for start, end in matches]
            coords = sorted(coords, key=lambda x: x[0], reverse=True)
            for start, end in coords:
                text = text[:start] + censor_tag + text[end:]
            return text
        df['content'] = df.apply(censor_row, axis=1)
        return df
```
