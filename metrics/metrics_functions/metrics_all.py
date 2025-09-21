import json
from datetime import datetime
from typing import Dict, Any
import os
from concurrent.futures import ThreadPoolExecutor

from metrics_functions.rouge import calculate_rouge
from metrics_functions.meteor import calculate_meteor
from metrics_functions.bert_score import calculate_bertscore
from metrics_functions.word_overlap import calculate_word_overlap
from metrics_functions.entity_keyword import calculate_entity_keyword_recall
from metrics_functions.compression import calculate_compression_ratio
from metrics_functions.bart_score import calculate_bart_score

from langchain_openai import AzureChatOpenAI

from dotenv import load_dotenv

load_dotenv()
print(os.getenv("OPENAI_API_KEY"))
print(os.getenv("OPENAI_API_BASE"))

def load_markdown_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def evaluate_files(generated_file: str, reference_file: str) -> Dict[str, Any]:
    generated_text = load_markdown_file(generated_file)
    reference_text = load_markdown_file(reference_file)
    return evaluate_all(generated_text, reference_text)

def evaluate_all(generated: str, reference: str) -> Dict[str, Any]:
    results = {
        "evaluation_timestamp": datetime.now().isoformat(),
        "text_lengths": {
            "generated": len(generated),
            "reference": len(reference)
        },
    }

    def calculate_metric(metric_function, *args):
        return metric_function(*args)

    metrics = {
        "rouge": (calculate_rouge, generated, reference),
        "meteor": (calculate_meteor, generated, reference),
        "bertscore": (calculate_bertscore, generated, reference),
        "word_overlap": (calculate_word_overlap, generated, reference),
        "entity_keyword_recall": (calculate_entity_keyword_recall, generated, reference),
        "compression": (calculate_compression_ratio, generated, reference),
        "bart_score": (calculate_bart_score, generated, reference),
        "llm_evaluation": (evaluate_llm, generated, reference),
    }

    with ThreadPoolExecutor() as executor:
        future_to_metric = {
            executor.submit(calculate_metric, func, *args): name
            for name, (func, *args) in metrics.items()
        }

        for future in future_to_metric:
            metric_name = future_to_metric[future]
            try:
                results[metric_name] = future.result()
            except Exception as e:
                results[metric_name] = f"Error: {e}"

    return results

def evaluate_llm(generated: str, reference: str) -> str:
    llm = AzureChatOpenAI(
        azure_deployment=os.getenv("OPENAI_API_DEPLOYMENT_NAME"),
        api_version=os.getenv("OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_API_BASE")
    )

    messages=[
        ("system", "You are a helpful assistant that evaluates the quality of documents."),
        ("user",f"""Read the following files and decide which one contains the most useful information.
        Evaluate the content and the quality of the document.
        File 1: {generated}
        File 2: {reference}
        The result should be: FILE 1 or FILE 2, and the reasons for the choice (max 10 words).
        Only output the result in JSON format.""")
                ]
    
    message = llm.invoke(messages)
    print(message.content)
    return message.content



def save_results(results: Dict[str, Any], filepath: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"Results saved to {filepath}")
