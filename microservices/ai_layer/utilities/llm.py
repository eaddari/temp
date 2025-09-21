from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI

load_dotenv(r"C:\desktopnoonedrive\docgenofficial\AIDocGen\.env", override=True)

llm = AzureChatOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    temperature=0.1
)