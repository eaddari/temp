from datetime import datetime
from typing import Any, Dict

def save_result(result: Dict[str, Any], filename: str = None) -> str:
    """Save the generated documentation to a file"""
    if not filename:
        filename = f"outputs\\doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(result.get("document", ""))
    
    return filename