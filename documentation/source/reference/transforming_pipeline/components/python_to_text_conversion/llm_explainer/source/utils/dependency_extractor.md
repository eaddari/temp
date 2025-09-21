# microservices.transforming_pipeline.components.python_to_text_conversion.llm_explainer.source.utils.dependency_extractor

Source file: `microservices\transforming_pipeline\components\python_to_text_conversion\llm_explainer\source\utils\dependency_extractor.py`

## Source Code

```python
import re
from typing import List, Dict

def extract_local_dependencies(file_content: str, repo_root: str = "src") -> List[Dict[str, str]]:
    """
    Extracts internal module dependencies from Python source code.

    Args:
        file_content (str): Full content of a Python file.
        repo_root (str): Root folder for project modules (e.g., 'src').

    Returns:
        List[Dict[str, str]]: A list of dictionaries each containing:
            - 'symbol': the imported symbol name
            - 'from': the source file where the symbol is defined
    """
    dependencies = []

    for match in re.findall(rf"from\s+({repo_root}(?:\.[\w]+)+)\s+import\s+([\w, ]+)", file_content):
        module_path, symbols = match
        source = module_path.replace(".", "/") + ".py"
        for symbol in map(str.strip, symbols.split(",")):
            dependencies.append({"symbol": symbol, "from": source})

    for match in re.findall(rf"import\s+({repo_root}(?:\.[\w]+)+)", file_content):
        source = match.replace(".", "/") + ".py"
        symbol = match.split(".")[-1]
        dependencies.append({"symbol": symbol, "from": source})

    return dependencies

```
