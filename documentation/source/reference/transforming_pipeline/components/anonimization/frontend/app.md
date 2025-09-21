# microservices.transforming_pipeline.components.anonimization.frontend.app

Source file: `microservices\transforming_pipeline\components\anonimization\frontend\app.py`

## Source Code

```python
import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed

class AnonimizatorAzure:
    def __init__(self):
        load_dotenv()
        self.subscription_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.api_version = os.getenv("AZURE_OPENAI_VERSION")
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.azure_model_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

        self.SYSTEM_PROMPT = (
            """
            You are a data anonymization assistant. 
            Identify and replace all personal information (PII) such as names, emails, 
            phone numbers, addresses, as well as any API keys, access tokens, secrets, passwords, and credentials 
            with tags like: <PERSON>, <EMAIL>, <PHONE_NUMBER>, <ADDRESS>, <API_KEY>, 
            <TOKEN>, <PASSWORD>. Do not change anything else in the text.
            """
        )

    def llm_parquet_anonimizer(self, text: str) -> str:
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

    def parallel_anonimization(self, df: pd.DataFrame) -> pd.DataFrame:
        test_row = {"name": ".env", "content": "api_key=akd1239u8190ue101jodjakn1090123098dyq"}
        df = pd.concat([pd.DataFrame([test_row]), df], ignore_index=True)

        texts = df["content"].tolist()
        max_workers = 8
        results = [None] * len(texts)

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_idx = {executor.submit(self.llm_parquet_anonimizer, text): idx for idx, text in enumerate(texts)}
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                try:
                    results[idx] = future.result()
                except Exception as e:
                    results[idx] = f"<ERROR: {str(e)}>"

        df["content"] = results
        return df

st.set_page_config(page_title="🔐 Parquet Anonymizer", layout="wide")
st.title("Azure OpenAI - Parquet Anonymizer")

uploaded_file = st.file_uploader("Carica un file .parquet", type=["parquet"])

if uploaded_file:
    try:
        df_originale = pd.read_parquet(uploaded_file)

        if "content" not in df_originale.columns:
            st.error("Il file deve contenere una colonna 'content'.")
        else:
            st.subheader("Contenuto originale del file")
            st.dataframe(df_originale, use_container_width=True)

            if st.button("Anonimizza contenuti"):
                with st.spinner("Anonimizzazione in corso con Azure OpenAI..."):
                    anonymizer = AnonimizatorAzure()
                    df_anonimizzato = anonymizer.parallel_anonimization(df_originale.copy())

                st.success("Anonimizzazione completata")
                st.subheader("Contenuto anonimizzato")
                st.dataframe(df_anonimizzato, use_container_width=True)

    except Exception as e:
        st.error(f"Errore nella lettura/parsing del file: {str(e)}")

```
