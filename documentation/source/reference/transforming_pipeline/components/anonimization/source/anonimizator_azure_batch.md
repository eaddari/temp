# microservices.transforming_pipeline.components.anonimization.source.anonimizator_azure_batch

Source file: `microservices\transforming_pipeline\components\anonimization\source\anonimizator_azure_batch.py`

## Source Code

```python
import os
import pandas as pd
from dotenv import load_dotenv
from openai import AzureOpenAI
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from microservices.transforming_pipeline.components.anonimization.utils.anonymization_prompt import SYSTEM_PROMPT
from azure.storage.blob.aio import ContainerClient, BlobServiceClient
import asyncio

class AnonimizatorAzure:

    def __init__(self):
        load_dotenv()
        self.subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = os.getenv("AZURE_OPENAI_VERSION")
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_model_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
        self.SYSTEM_PROMPT = SYSTEM_PROMPT

    def generate_jsonl_for_batch(self, df: pd.DataFrame, jsonl_path: str) -> None:
        """
        Generate a .jsonl file for Azure OpenAI batch processing from a DataFrame.
        Each line is a chat completion request.
        """
        import json
        with open(jsonl_path, "w", encoding="utf-8") as f:
            for idx, row in df.iterrows():
                body = {
                    "model": self.azure_model_deployment,
                    "messages": [
                        {"role": "system", "content": self.SYSTEM_PROMPT},
                        {"role": "user", "content": row["content"]}
                    ]
                }
                entry = {
                    "custom_id": f"task-{idx}",
                    "method": "POST",
                    "url": "/chat/completions",
                    "body": body
                }
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    async def submit_batch_job(self, input_blob_url: str, output_container_url: str) -> str:
        """
        Submit a batch job to Azure OpenAI using the batch API.
        Returns the job ID.
        """
        from azure.identity import DefaultAzureCredential
        credential = DefaultAzureCredential()
        client = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            azure_ad_token_provider=lambda: credential.get_token("https://cognitiveservices.azure.com/.default").token,
            api_version=self.api_version
        )
        try:
            with open("input_batch.jsonl", "rb") as f:
                file_response = client.files.create(file=f, purpose="batch")
            file_id = file_response.id
            response = client.batches.create(
                completion_window='24h',
                endpoint='/v1/chat/completions',
                input_file_id=file_id
            )
            print(f"Batch job submitted. Job ID: {response.id}")
            return response.id
        finally:
            client.close()

    async def monitor_batch_job(self, job_id: str, poll_interval: int = 60) -> None:
        """
        Monitor the batch job status until completion.
        """
        from azure.identity import DefaultAzureCredential
        import time
        credential = DefaultAzureCredential()
        client = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            azure_ad_token_provider=lambda: credential.get_token("https://cognitiveservices.azure.com/.default").token,
            api_version=self.api_version
        )
        try:
            while True:
                status = client.batches.retrieve(job_id).status
                print(f"Job Status: {status}")
                if status in ["completed", "failed", "cancelled"]:
                    break
                time.sleep(poll_interval)
        finally:
            client.close()

output_dir = "outputs"

def chunk_rows(rows, chunk_size):
    for i in range(0, len(rows), chunk_size):
        yield rows[i:i+chunk_size]

async def container_to_parquet(container_name: str, single_parquet: bool = False):
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    
    os.makedirs(output_dir, exist_ok=True)
    if single_parquet:
        rows = []
        async for blob in container_client.list_blobs():
            blob_client = container_client.get_blob_client(blob.name)
            stream = await blob_client.download_blob()
            blob_data = await stream.readall()
            try:
                content = blob_data.decode('utf-8')
            except Exception:
                content = str(blob_data)
            rows.append({
                "name": blob.name,
                "content": content
            })
        chunk_size = 1000000
        parquet_path = []
        for idx, chunk in enumerate(chunk_rows(rows, chunk_size)):
            df = pd.DataFrame(chunk)
            output_path = os.path.join(output_dir, f"{container_name}_part_{idx}.parquet")
            df.to_parquet(output_path)
            parquet_path.append(output_path)
        first_parquet_path = parquet_path[0] if parquet_path else ""
        return {
            "status": True,
            "details": f"Container {container_name} converted to Parquet and saved to {output_dir}",
            "parquet_path": first_parquet_path,
            "files": [{"name": row["name"], "content": row["content"]} for row in rows]
        }

async def upload_input_blob(blob_service_client, input_container, input_blob_name, local_path):
    input_container_client = blob_service_client.get_container_client(input_container)
    try:
        await input_container_client.create_container()
    except Exception:
        pass
    with open(local_path, "rb") as data:
        await input_container_client.upload_blob(input_blob_name, data, overwrite=True)
    print(f"Uploaded {input_blob_name} to Azure Blob Storage: {input_container}/{input_blob_name}")

async def main():

    input_parquet = "C:\\desktopnoonedrive\\docgenofficial\\AIDocGen\\docgen-unofficial-docgen-test_part_0.parquet"
    df = pd.read_parquet(input_parquet)
    anonimizator = AnonimizatorAzure()
    anonimizator.generate_jsonl_for_batch(df, "input_batch.jsonl")
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    async with BlobServiceClient.from_connection_string(connection_string) as blob_service_client:
        input_container = "batch-input"
        input_blob_name = "input_batch.jsonl"
        await upload_input_blob(blob_service_client, input_container, input_blob_name, "input_batch.jsonl")
        job_id = await anonimizator.submit_batch_job(
            input_blob_url=f"https://docgentest.blob.core.windows.net/{input_container}/{input_blob_name}",
            output_container_url="https://docgentest.blob.core.windows.net/batchanonimization"
        )
        await anonimizator.monitor_batch_job(job_id)
        await container_to_parquet("batchanonimization", single_parquet=True)

if __name__ == "__main__":
    asyncio.run(main())
```
