# microservices.transforming_pipeline.components.python_to_text_conversion.llm_explainer.testing.performance_models

Source file: `microservices\transforming_pipeline\components\python_to_text_conversion\llm_explainer\testing\performance_models.py`

## Source Code

```python
import pandas as pd
import sys
import os

# Add the project root to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from components.python_to_text_conversion.llm_explainer.source.python_explainer import CodeExplainer

# Ensure results directory
RESULTS_DIR = os.path.join(SCRIPT_DIR, "performance_results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# Filter only .py files in the specific subdirectory
TARGET_DIR = "microservices/input_integration_pipeline/source/repo_downloader"
parquet_path = os.path.abspath(os.path.join(PROJECT_ROOT, "..", "..", "docgen-unofficial-docgen-test_part_0.parquet"))
df = pd.read_parquet(parquet_path)
df_py = df[df["name"].str.endswith(".py") & df["name"].str.startswith(TARGET_DIR.replace("\\", "/"))]

# Initialize explainers
models = {
    "gpt-4.1": CodeExplainer(model="gpt-4.1"),
    "gpt-4.1-nano": CodeExplainer(model="gpt-4.1-nano"),
    "gpt-4.1-mini": CodeExplainer(model="gpt-4.1-mini"),
    "gpt-4o": CodeExplainer(model="gpt-4o")
}

# Apply each explainer and join the results by 'name'
df_out = df_py[["name"]].copy()
for model_name, explainer in models.items():
    result_df = explainer.explain_dataframe(df_py)
    result_df = result_df.rename(columns={"content": model_name})
    df_out = df_out.merge(result_df[["name", model_name]], on="name", how="left")

# Save final merged output
output_path = os.path.join(RESULTS_DIR, "comparison_results.parquet")
df_out.to_parquet(output_path, index=False)

```
