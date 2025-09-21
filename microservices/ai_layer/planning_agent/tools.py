import os
import json
from planning_agent.utils.clean_json import _clean_json_response
from langchain.tools import Tool
from langchain_core.output_parsers import StrOutputParser

from utilities.llm import llm
from query_agent.tools import get_graph_schema
from planning_agent.prompts import analysis_prompt, planning_prompt, readme_planning_prompt


def analyze_documentation_request(request: str) -> str:
    """Analyze a documentation request to understand requirements."""
    try:
        schema = get_graph_schema()
        
        analysis_chain = analysis_prompt | llm | StrOutputParser()
        analysis = analysis_chain.invoke({
            "user_request": request,
            "schema": schema
        })
        
        return analysis
        
    except Exception as e:
        return f"Error analyzing request: {str(e)}"

def create_documentation_plan(request: str) -> str:
    """Create a detailed plan for generating documentation based on the request."""
    try:
        schema = get_graph_schema()
        
        analysis = analyze_documentation_request(request)

        planning_chain = planning_prompt | llm | StrOutputParser()
        plan_result = planning_chain.invoke({
            "analysis": analysis,
            "user_request": request,
            "schema": schema
        })
        
        plan_result = _clean_json_response(plan_result)

        json.loads(plan_result)
        return plan_result
        
    except Exception as e:
        return f"Error creating plan: {str(e)}"
    
def create_readme_plan(request: str) -> str:
    """Create a detailed plan for generating a README based on the request."""
    try:
        schema = get_graph_schema()
        
        # First analyze the request
        analysis = analyze_documentation_request(request)

        planning_chain = readme_planning_prompt | llm | StrOutputParser()
        plan_result = planning_chain.invoke({
            "analysis": analysis,
            "user_request": request,
            "schema": schema
        })
        
        plan_result = _clean_json_response(plan_result)

        json.loads(plan_result)
        return plan_result
        
    except Exception as e:
        return f"Error creating plan: {str(e)}"

def validate_documentation_plan(plan_json: str) -> str:
    """Validate a documentation plan and provide improvement suggestions."""

    plan = json.loads(plan_json)
        
    validation_results = {
        "is_valid": True,
        "issues": [],
        "suggestions": [],
        "improved_plan": plan
    }
    
    required_fields = ["document_info", "sections"]
    for field in required_fields:
        if field not in plan:
            validation_results["is_valid"] = False
            validation_results["issues"].append(f"Missing required field: {field}")
    
    if "sections" in plan:
        for i, section in enumerate(plan["sections"]):
            if "section_name" not in section:
                validation_results["issues"].append(f"Section {i+1} missing name")
            if "queries" not in section or not section["queries"]:
                validation_results["suggestions"].append(f"Section '{section.get('section_name', f'Section {i+1}')}' has no queries")
    
    return json.dumps(validation_results, indent=2)


def get_schema_information(input_str: str = "") -> str:
    """Get information about the available graph schema."""
    return get_graph_schema()


planning_tools = [
    Tool(
        name="AnalyzeRequest",
        func=analyze_documentation_request,
        description="Analyze a documentation request to understand requirements, scope, and target audience."
    ),
    Tool(
        name="CreatePlan",
        func=create_documentation_plan,
        description="Create a detailed documentation plan with sections, queries, and structure."
    ),
        Tool(
            name="CreateREADMEPlan",
            func=create_readme_plan,
            description="Create a detailed README plan with sections, queries, and structure."
        ),

    Tool(
        name="ValidatePlan",
        func=validate_documentation_plan,
        description="Validate a documentation plan and provide improvement suggestions."
    ),
    Tool(
        name="GetSchemaInfo",
        func=get_schema_information,
        description="Get information about the available graph database schema."
    )
]
