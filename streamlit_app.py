import streamlit as st
import requests

import math


math.cos

st.title("Pipeline Step Selector")

def get_step_states():
    file_converter = st.checkbox("File Converter")
    python_to_text = st.checkbox("Python to Text")
    text_cleaner = st.checkbox("Text Cleaner")
    return {
        "file_converter": file_converter,
        "python_to_text": python_to_text,
        "text_cleaner": text_cleaner
    }

step_states = get_step_states()

input_path = st.text_input("Input Parquet Path", "your_input.parquet")
keep_comments = st.checkbox("Keep Comments", value=True)

if st.button("Run Pipeline"):
    payload = {
        "input_path": input_path,
        "keep_comments": keep_comments,
        "step_states": step_states
    }
    try:
        api_url = "http://localhost:5002/v5/transforming_pipeline"
        response = requests.post(api_url, json=payload)
        st.write(response.json())
    except Exception as e:
        st.error(f"Error: {e}")
