def _clean_json_response(response: str) -> str:
    """Clean LLM response to extract valid JSON."""
    import re
    response = re.sub(r'```json\s*', '', response)
    response = re.sub(r'```\s*$', '', response)
    
    start = response.find('{')
    end = response.rfind('}') + 1
    
    if start != -1 and end > start:
        return response[start:end]
    
    return response.strip()
