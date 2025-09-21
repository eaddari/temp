# microservices.transforming_pipeline.source.splitter

Source file: `microservices\transforming_pipeline\source\splitter.py`

## Source Code

```python

import asyncio
import inspect
import pandas as pd
from components.anonimization.source.anonimizator_localization_copy import AnonimizatorLocalization
from components.python_to_text_conversion.filtering.source.cleaner_comments import cleaner
from components.python_to_text_conversion.filtering.source.convert_notebook import converter
from components.md_to_txt.source.converter import FileConverter
from components.cleaning_and_transformation.source.text_cleaner import TextCleaner
from components.python_to_text_conversion.llm_explainer.source.python_explainer import CodeExplainer
import json

json_path = "pipeline_extensions.json"

with open(json_path, "r", encoding="utf-8") as f:
    EXTENSIONS = json.load(f)

class ManageTransforming():
    def __init__(self, input_path: str, keep_comments: bool, ):
        self.input_path = input_path
        self.keep_comments = keep_comments
        self.df = pd.read_parquet(self.input_path)
        self.config = EXTENSIONS
        self.step_handlers = {
            "anonymization": self._anonymization,
            "file_converter": self._file_converter,
            "python_to_text": self._python_to_text,
            "text_cleaner": self._text_cleaner
        }

    def __filter_extension(self, extensions) -> pd.DataFrame:
        """Filter the DataFrame for the specified extensions."""
        mask = self.df['name'].apply(lambda x: any(str(x).endswith(ext) for ext in extensions))
        filtered_df = self.df[mask]
        return filtered_df

    def _anonymization(self) -> pd.DataFrame:
        """Anonymize the DataFrame using found coordinates"""
        anonymizer = AnonimizatorLocalization()
        print("Starting anonymization...")
        df = anonymizer.run_anonimizer_in_chunks(self.df, chunk_size=40)
        df = anonymizer.censor_content(df, content_col='content', coords_col='coordinates').drop(columns=['coordinates'], errors='ignore')
        self.df = df
        print("Anonymization completed.")
        return self.df
    
    async def _file_converter(self) -> pd.DataFrame:
        exts = self.config.get("file_converter", [])
        converter = FileConverter(self.df, exts)
        updated_df = await converter.file_to_text()
        self.df['content'] = updated_df['content']
        return self.df

    async def _python_to_text(self) -> pd.DataFrame:
        exts = self.config.get("python_to_text", [])
        mask = self.df['name'].apply(lambda x: any(str(x).endswith(ext) for ext in exts))
        
        self.df.loc[mask, 'content'] = self.df.loc[mask, 'content'].apply(converter)

        if not self.keep_comments:
            self.df.loc[mask, 'content'] = cleaner(self.df.loc[mask, 'content'])
        
        print("Explaining Python code...")

        explained_df = CodeExplainer().explain_dataframe(self.df.loc[mask])

        self.df.loc[mask, 'content'] = explained_df['content']
        
        return self.df

    async def _text_cleaner(self) -> pd.DataFrame:
        exts = self.config.get("text_cleaner", [])
        df = self.__filter_extension(exts)
        if df is None or df.empty:
            print("No data to clean.")
            return self.df
        print("Cleaning text data...")
        try:
            self.df = TextCleaner(self.df).save_cleaned_df()
        except Exception as e:
            print(f"Error occurred while cleaning text data: {e}")
            return self.df
        return self.df
    
    async def run_step(self, step_name: str) -> pd.DataFrame:
        """Run a specific pipeline step by name."""
        handler = self.step_handlers.get(step_name)
        if handler:
            if inspect.iscoroutinefunction(handler):
                return await handler()
            else:
                return handler()
        else:
            raise ValueError(f"Unknown step: {step_name}")

    async def run_steps(self, steps: list[str]) -> dict:
        """Run multiple pipeline steps and return the final DataFrame."""
        for step in steps:
            print(f"Running step: {step}")
            self.df = await self.run_step(step)
        self.df.to_parquet(f"{self.input_path.replace('.parquet','')}_processed.parquet")
        return {"message": "Pipeline executed successfully.", "path":f"{self.input_path.replace('.parquet','')}_processed.parquet"}
```
