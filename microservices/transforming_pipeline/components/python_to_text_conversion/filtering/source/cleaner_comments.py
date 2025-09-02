import pandas as pd
import re

def remove_comments_and_docstrings(code: str) -> str:
    """
    Removes comments and docstrings from a given Python source code string.

    Parameters:
        code (str): A string containing Python source code.

    Returns:
        code (str): The output code with all comments and docstrings removed.
    """
    code = re.sub(r'("""|\'\'\')(?:.|\n)*?\1', '', code)
    code = re.sub(r'#.*', '', code)
    return code 
    
def cleaner(content: list) -> list:
    """
    Applies the `remove_comments_and_docstrings` function to each element in a list-like object.

    Parameters:
        content (list): A list-like object (e.g., pandas Series) containing strings of Python code.

    Returns:
        content (list): A list with comments and docstrings removed from each code string.
    """
    content = content.apply(remove_comments_and_docstrings)
    return content
