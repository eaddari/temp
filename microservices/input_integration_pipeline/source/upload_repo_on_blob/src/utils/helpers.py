import re
import os
import pandas as pd

def sanitize_container_name(name: str) -> str:
    """
    Sanitizes a string to produce a valid Azure Blob Storage container name.

    Rules enforced:
    - Must be between 3 and 63 characters long.
    - Must contain only lowercase letters, numbers, and hyphens.
    - Must begin and end with a letter or a number.
    - Hyphens must be surrounded by letters or numbers (no leading/trailing hyphens, no consecutive hyphens).

    If the cleaned name does not meet these criteria, a fallback UUID-based name is generated.

    Args:
        name (str): The input string, typically a folder or repository name.

    Returns:
        str: A valid Azure container name.
    """
    name = re.sub(r'[^a-z0-9-]', '-', name.lower())
    name = re.sub(r'-{2,}', '-', name)
    name = name.strip('-')
    name = name[:63].strip('-')  

    return name

def search_config(nome_file):
    base_dir = "/app"
    for cartella_corrente, _, files in os.walk(base_dir):
        for f in files:
            if f == nome_file:
                return os.path.join(cartella_corrente, f)


def is_path_allowed(relative_path: str) -> bool:
    """
    Checks if a file path is allowed for upload.

    Args:
        relative_path (str): File path relative to the repository root.

    Returns:
        bool: True if allowed, False otherwise.
    """
    path = search_config("config.json")
    EXCLUDED_DIRS = pd.read_json(path)["languages"]["python"]["EXCLUDED_DIRS"]
    ALLOWED_EXTENSIONS = pd.read_json(path)["languages"]["python"]["ALLOWED_EXTENSIONS"]
    parts = relative_path.split("/")
    if any(part in EXCLUDED_DIRS for part in parts):
        return False
    _, ext = os.path.splitext(relative_path)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        return False
    return True
