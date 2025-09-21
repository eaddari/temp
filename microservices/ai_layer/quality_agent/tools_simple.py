import json
from utilities.llm import llm
from langchain.tools import Tool

def assess_document_quality(document_text: str) -> str:
    """Assess document quality and return JSON with scores."""
    prompt = f"""
    Evaluate this document and provide a quality assessment as JSON:
    
    Document:
    {document_text}
    
    Provide your assessment as JSON:
    {{
        "overall_score": 0.0,
        "final_score": 0.0,
        "scores": [
            {{"criterion": "completeness", "score": 0.0, "feedback": "feedback text"}},
            {{"criterion": "accuracy", "score": 0.0, "feedback": "feedback text"}},
            {{"criterion": "clarity", "score": 0.0, "feedback": "feedback text"}}
        ],
        "summary": "Overall assessment summary",
        "recommendations": ["improvement recommendation 1"]
    }}
    """
    
    try:
        response = llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        return f"Error assessing quality: {str(e)}"

tools = [
    Tool(
        name="AssessQuality",
        func=assess_document_quality,
        description="Assess document quality and return structured quality scores and feedback."
    )
]