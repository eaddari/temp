from langchain.tools import Tool
from generation_agent.prompts import content_prompt
from query_agent.tools import tools as query_tools
from utilities.llm import llm
from langchain_core.output_parsers import StrOutputParser

def generate_single_section(request: str) -> str:

    lines = request.split('\n')
    
    current_section_name = lines[0].replace("Generate useful content for the section: ", "").strip()
    
    neo4j_tool = None
    for tool in query_tools:
        if "neo4j" in tool.name.lower() or "query" in tool.name.lower():
            neo4j_tool = tool
            break
    
    if neo4j_tool:

        query_prompt = f"Find information relevant for '{current_section_name}' in the documentation"
        graph_data = neo4j_tool.func(query_prompt)
    else:
        graph_data = "No specific data found in codebase."
    
    content_chain = content_prompt | llm | StrOutputParser()
    
    section_content = content_chain.invoke({
        "section_name": current_section_name,
        "graph_data": graph_data,
        "user_request": request
    })
    
    return f"## {current_section_name}\n\n{section_content}"

tools = [
    Tool(
        name="GenerateSingleSection",
        func=generate_single_section,
        description="Generate content for a single section using graph data from the codebase."
    )
]