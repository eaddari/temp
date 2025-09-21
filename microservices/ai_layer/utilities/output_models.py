from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser
import re


class DocumentSection(BaseModel):
    """Model for individual document sections"""
    section_name: str = Field(description="Name of the section")
    content_type: Optional[str] = Field(description="Type of content (overview, analysis, etc.)", default=None)
    priority: Optional[str] = Field(description="Priority level (High, Medium, Low)", default="Medium")
    description: Optional[str] = Field(description="Description of what this section contains", default="")


class PlanningOutput(BaseModel):
    """Structured output for planning agent"""
    title: str = Field(description="Title of the documentation")
    sections: List[DocumentSection] = Field(description="List of planned sections")
    description: Optional[str] = Field(description="Brief description of the document", default="")
    estimated_length: Optional[str] = Field(description="Estimated document length", default="Medium")


class GenerationOutput(BaseModel):
    """Structured output for generation agent"""
    content: str = Field(description="Generated content for the section")
    section_title: Optional[str] = Field(description="Title of the generated section", default="")
    word_count: Optional[int] = Field(description="Approximate word count", default=0)


class QualityScore(BaseModel):
    """Individual quality assessment score"""
    criterion: str = Field(description="Name of the quality criterion")
    score: float = Field(description="Score from 0-10")
    feedback: str = Field(description="Detailed feedback for this criterion")


class QualityOutput(BaseModel):
    """Structured output for quality agent"""
    overall_score: float = Field(description="Overall quality score (0-10)")
    final_score: float = Field(description="Final normalized score (0-10)")
    scores: List[QualityScore] = Field(description="Individual criterion scores")
    summary: str = Field(description="Overall quality assessment summary")
    recommendations: List[str] = Field(description="List of improvement recommendations", default_factory=list)


def extract_json_from_final_answer(text: str) -> str:
    """Extract JSON content from Final Answer section or find JSON block in text"""
    if not text.strip():
        return "{}"
        
    match = re.search(r'Final Answer:\s*(.+)', text, re.DOTALL)
    if match:
        candidate = match.group(1).strip()
        if candidate.startswith('{') and candidate.endswith('}'):
            return candidate
    
    json_match = re.search(r'(\{.*\})', text, re.DOTALL)
    if json_match:
        return json_match.group(1).strip()
    
    return "{}"

planning_parser = PydanticOutputParser(pydantic_object=PlanningOutput)
generation_parser = PydanticOutputParser(pydantic_object=GenerationOutput)
quality_parser = PydanticOutputParser(pydantic_object=QualityOutput)
