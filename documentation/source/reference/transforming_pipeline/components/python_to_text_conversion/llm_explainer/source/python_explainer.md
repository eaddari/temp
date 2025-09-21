# microservices.transforming_pipeline.components.python_to_text_conversion.llm_explainer.source.python_explainer

Source file: `microservices\transforming_pipeline\components\python_to_text_conversion\llm_explainer\source\python_explainer.py`

## Source Code

```python
import os
from typing import List, Dict
import pandas as pd
from openai import AzureOpenAI
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from .utils.prompt import SYSTEM_PROMPT
from .utils.dependency_extractor import extract_local_dependencies

class CodeExplainer:
    """
    Handles the transformation of Python code into natural language explanations
    using Azure OpenAI. Supports parallel processing of multiple files.
    """

    def __init__(self, max_workers: int = 8, model: str = None):
        """
        Initializes the CodeExplainer with model credentials and parameters.

        Attributes:
            system_prompt (str): The system prompt used for guiding the model output.
            max_workers (int): The number of threads for parallel execution.
            model (str): The model's name you want to use.
        """
        load_dotenv()
        self.client = AzureOpenAI(
            api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        )
        self.model = model or os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.system_prompt = SYSTEM_PROMPT
        self.max_workers = max_workers

    def explain_code(self, code: str, file_path: str) -> str:
        """
        Generates a natural language explanation for a given Python file.

        Args:
            code (str): Source code of the file.
            file_path (str): File path for context.

        Returns:
            str: Model-generated explanation of the code.
        """
        deps = extract_local_dependencies(code)
        dep_lines = [f"- {d['symbol']} from {d['from']}" for d in deps]
        dep_block = (
            "This file depends on the following internal components:\n" +
            "\n".join(dep_lines) + "\n\n"
            if dep_lines else ""
        )

        user_prompt = (
            f"{dep_block}"
            f"You are given the full content of the Python file `{file_path}`:\n\n"
            f"{code}"
        )

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
            model=self.model
        )
        return response.choices[0].message.content

    def _process_row(self, row: pd.Series) -> str:
        """
        Processes a single DataFrame row by invoking the explanation method.

        Args:
            row (pd.Series): A row with 'name' and 'content' keys.

        Returns:
            str: Natural language explanation of the code in the row.
        """
        print(f"Explaining: {row['name']}")
        return self.explain_code(row["content"], row["name"])

    def explain_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generates explanations for a DataFrame containing Python source files.

        Args:
            df (pd.DataFrame): DataFrame with 'name' and 'content' columns.

        Returns:
            pd.DataFrame: New DataFrame with 'name' and explained 'content'.
        """
        results = [""] * len(df)
        names = df["name"].tolist()
        rows = df.to_dict(orient="records")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(self._process_row, pd.Series(row)): idx
                for idx, row in enumerate(rows)
            }
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    results[idx] = future.result()
                except Exception as e:
                    results[idx] = f"Error: {str(e)}"

        return pd.DataFrame({"name": names, "content": results})

```
