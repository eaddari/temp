# microservices.transforming_pipeline.components.anonimization.source.anonimizator_ner_pii

Source file: `microservices\transforming_pipeline\components\anonimization\source\anonimizator_ner_pii.py`

## Source Code

```python
import os
import dotenv
import pandas as pd
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
dotenv.load_dotenv()

# Load your Azure credentials from environment variables or set them directly
endpoint = os.getenv("TEXT_ANALYTICS_ENDPOINT")
key = os.getenv("TEXT_ANALYTICS_API_KEY")

# Authenticate client
client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def detect_pii(df, text_column):
    results = []
    documents = df[text_column].tolist()
    batch_size = 5
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        response = client.recognize_pii_entities(batch)
        for doc, res in zip(batch, response):
            if not res.is_error:
                entities = [(e.text, e.category, e.subcategory) for e in res.entities]
                results.append({"text": doc, "pii_entities": entities})
            else:
                results.append({"text": doc, "error": str(res.error)})
    return pd.DataFrame(results)

if __name__ == "__main__":
    input_parquet = "C:/desktopnoonedrive/docgenofficial/AIDocGen/docgen-unofficial-docgen-test_part_0.parquet"
    df = pd.read_parquet(input_parquet)
    result_df = detect_pii(df, text_column="content")
    result_df.to_parquet("pii_results.parquet", index=False)
    print("PII detection complete. Results saved to pii_results.parquet.")

```
