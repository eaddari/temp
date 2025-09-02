from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import Optional

import os
import pandas as pd

load_dotenv()
"""
def explainer_code(dataset: pd.DataFrame, models: list):
    temp = dataset.copy()
    for model in models:
        model_name = str(model)
        code_explainer = CodeExplainer(model=model)
        explained_df = code_explainer.explain_dataframe(temp)
        explained_df = explained_df.rename(columns={'content': model_name})
        dataset = pd.merge(dataset, explained_df, on="name")

    dataset.to_parquet("standalone_converter/data/explained_code.parquet")
"""
class Judge():
    def __init__(self,
            model: str,
            system_prompt: str, 
            api_key: Optional[str] = None, 
            azure_endpoint: Optional[str] = None,
            api_version: Optional[str] = None
        ):
        self.system_prompt = system_prompt
        self.api_key, self.azure_endpoint = api_key, azure_endpoint
        self.azure_deployment, self.api_version = model, api_version
        self.llm = self.__create_istance()
        self.llm = self.__create_chain()


    def __create_istance(self) -> AzureChatOpenAI:
        return AzureChatOpenAI(
            api_key = self.api_key or os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint = self.azure_endpoint or os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_deployment = self.azure_deployment,  
            api_version = self.api_version or os.getenv("AZURE_OPENAI_API_VERSION")
        )
    
    def __create_chain(self):
        prompt = ChatPromptTemplate.from_messages([(
                "system",
                self.system_prompt
            )]
        )

        return prompt | self.llm
    
    def start_evaluation(self, source_code: str, generated_explanation: str) -> str:
        return self.llm.invoke(
            {
                "source_code": source_code,
                "generated_explanation": generated_explanation,
            }
        ).content