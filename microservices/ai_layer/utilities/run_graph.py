from typing import Any, Dict
from langgraph.graph import StateGraph

def run_documentation_generation(user_request: str, state_graph: StateGraph) -> Dict[str, Any]:
    """Run the documentation generation workflow"""
    
    initial_state = {
        "user_request": user_request,
        "plan": "",
        "sections": [],
        "current_section_index": 0,
        "document": "",
        "quality_score": 0.0,
        "quality_threshold": 7.0,
        "messages": [],
        "generated_sections": []
    }
    
    result = state_graph.invoke(initial_state)
    
    return result