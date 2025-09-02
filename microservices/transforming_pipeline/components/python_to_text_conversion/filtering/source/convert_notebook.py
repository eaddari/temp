import pandas as pd
import json

def converter(source: str) -> str:
    """
    Convert notebook to script Python.

    Parameters:
        code (str): A string containing notebook Python source code.

    Returns:
        content (str): The output code converted.
    """
    content = "\n".join(["".join(code["source"]) for code in json.load(source)["cells"]])
    return content