import os
import pandas as pd
from dotenv import load_dotenv
from openai import AzureOpenAI
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from microservices.transforming_pipeline.components.anonimization.utils.anonymization_prompt import SYSTEM_PROMPT

class AnonimizatorAzure:
    """
    This class is used to anonymize a parquet file using 
    the Azure OpenAI API in parallel using gpt-4.1-mini model.

    Attributes:     
        subscription_key (str): Azure OpenAI API key
        api_version (str): Azure OpenAI API version
        azure_endpoint (str): Azure OpenAI API endpoint
        azure_model_deployment (str): Azure OpenAI API model deployment
        client (AzureOpenAI): Azure OpenAI API client
        script_dir (str): Script directory where the script is located 
        data_dir (str): Data directory where the input .parquet file is located
        input_file (str): Input .parquet file
        input_filename (str): Input filename of the input .parquet file
        output_filename (str): Output filename of the anonimized .parquet file
        output_file (str): Output .parquet anonimized file 
        df (pd.DataFrame): DataFrame converted from the input .parquet file
        SYSTEM_PROMPT (str): System prompt for the LLM
    """
    def __init__(self):
        load_dotenv()
        self.subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = os.getenv("AZURE_OPENAI_VERSION")
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_model_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.SYSTEM_PROMPT = SYSTEM_PROMPT
        #self.script_dir = os.path.dirname(os.path.abspath(__file__)) # TODO: 
        #self.data_dir = os.path.join(self.script_dir, "..", "data") # TODO: 
        #self.input_file = os.path.join(self.data_dir, "docgen-unofficial-docgen-test_part_0.parquet") # TODO: 
        #self.input_filename = os.path.basename(self.input_file) # TODO: 
        #self.output_filename = self.input_filename.replace(".parquet", "_anonimized.parquet") # TODO: 
        #self.output_file = os.path.join(self.data_dir, self.output_filename) # TODO: 
        #self.df = pd.read_parquet(self.input_file) # TODO: 
        
        

    def llm_parquet_anonimizer(self, text: str) -> str:
        """
        Anonymizes a given text using the Azure OpenAI API model gpt-4o-mini.

        Args:
            text (str): The text to anonymize with pii information 
            and api keys/tokens/secrets/passwords/etc.

        Returns:
            text (str): The anonymized text without pii information 
            and api keys/tokens/secrets/passwords/etc.
        """
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": text}
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
        return response.choices[0].message.content.strip()

    def parallel_anonimization(self, df: pd.DataFrame) -> None:
        """
        Anonymize a parquet file using the Azure OpenAI API.

        Args:
            df (pd.DataFrame): The DataFrame containing the data from the file parquet to anonymize

        Returns:
            None
        """
        
        texts = df["content"].tolist()
        max_workers = 16 
        results = [None] * len(texts)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_idx = {executor.submit(self.llm_parquet_anonimizer, text): idx for idx, text in enumerate(texts)}

            for future in tqdm(as_completed(future_to_idx), total=len(future_to_idx), desc="Anonimizing files ..."):
                idx = future_to_idx[future]

                try:
                    result = future.result()

                except Exception as exc:
                    print(f"Error in the row {idx}: {exc}")
                     
                results[idx] = result

        df["content"] = results
        df.to_parquet(self.output_file, index=False) # TODO: where to save?

        return df

if __name__ == "__main__":

    input_parquet = "C:\\desktopnoonedrive\\docgenofficial\\AIDocGen\\docgen-unofficial-docgen-test_part_0.parquet"

    df = pd.read_parquet(input_parquet)
    anonimizator = AnonimizatorAzure()
    anonimizator.parallel_anonimization(df)





