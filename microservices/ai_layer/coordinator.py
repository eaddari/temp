from dotenv import load_dotenv
from typing import TypedDict, Literal
from datetime import datetime

from langgraph.graph import StateGraph, START
from langgraph.types import Command

from planning_agent.planning_agent import planning_agent_runner as planning_agent
from generation_agent.tools import generate_single_section
from quality_agent.quality_agent import quality_agent_runner as quality_agent

from utilities.save_document import save_result
from utilities.run_graph import run_documentation_generation
from utilities.output_models import planning_parser, generation_parser, quality_parser, extract_json_from_final_answer

load_dotenv(r"C:\desktopnoonedrive\docgenofficial\AIDocGen\.env", override=True)

class DocumentationState(TypedDict):
    user_request: str
    plan: str
    sections: list
    current_section_index: int
    document: str
    quality_score: float
    quality_threshold: float
    messages: list
    generated_sections: list

def planning_node(state: DocumentationState) -> Command[Literal["generation_node", "quality_check_node"]]:
    """Planning agent node - creates documentation plan"""
    
    response = planning_agent.invoke({"input": f"{state['user_request']}"})
    
    plan_content = response.get("output", "")

    with open(f"outputs\\plan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w", encoding="utf-8") as f:
        f.write(plan_content)
    
    json_content = extract_json_from_final_answer(plan_content)
    parsed_plan = planning_parser.parse(json_content)
    sections = [section.section_name for section in parsed_plan.sections]
    
    return Command(
        goto="generation_node",
        update={
            "plan": plan_content,
            "sections": sections,
            "current_section_index": 0,
            "document": "",
            "generated_sections": [],
            "messages": state.get("messages", []) + [f"Planning completed: {len(sections)} sections"]
        }
    )

def generation_node(state: DocumentationState) -> Command[Literal["generation_node", "quality_check_node"]]:
    """Generation agent node - creates documentation content"""
    
    current_index = state['current_section_index']
    sections = state['sections']
    
    print(f"DEBUG: Current index: {current_index}, Total sections: {len(sections)}")
    
    if current_index >= len(sections):
        print("DEBUG: All sections completed, moving to quality check")
        return Command(
            goto="quality_check_node",
            update={
                "messages": state.get("messages", []) + [f"All {len(sections)} sections completed"]
            }
        )
    
    current_section = sections[current_index]
    print(f"DEBUG: Generating content for section '{current_section}'")
    
    generation_input = f"Generate useful content for the section: {current_section}\n"
    user_message = f"User request: {state['user_request']}\n"
    sections_for_context = f"Sections for context: {sections}"
    
    new_content = generate_single_section(generation_input+user_message+sections_for_context)
    
    if state['document']:
        updated_document = state['document'] + "\n\n" + new_content
    else:
        updated_document = new_content
    
    next_index = current_index + 1
    
    print(f"DEBUG: Section '{current_section}' completed.")
    
    return Command(
        goto="generation_node",
        update={
            "document": updated_document,
            "current_section_index": next_index,
            "messages": state.get("messages", []) + [f"Generated section {current_index + 1}/{len(sections)}: {current_section}"]
        }
    )

def quality_check_node(state: DocumentationState) -> Command[Literal["planning_node", "generation_node", "__end__"]]:
    """Quality check agent node - evaluates documentation quality"""

    response = quality_agent.invoke({"input": f"Score this document:\n{state['document']}"})
    quality_output = response.get("output", "Quality assessment completed.")
    json_content = extract_json_from_final_answer(quality_output)
    parsed_quality = quality_parser.parse(json_content)

    return Command(
        goto="__end__",
        update={
            "quality_score": parsed_quality.final_score,
            "messages": state.get("messages", []) + [f"Quality check completed: Final score {parsed_quality.final_score:.1f}/10"]
        }
    )

builder = StateGraph(DocumentationState)

builder.add_node(planning_node)
builder.add_node(generation_node)
builder.add_node(quality_check_node)
builder.add_edge(START, "planning_node")

graph = builder.compile()


if __name__ == "__main__":

    user_request = "Create a detailed and useful README"

    result = run_documentation_generation(user_request, graph)
    
    filename = save_result(result)

    print(f"Documentation saved to: {filename}")