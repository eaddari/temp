from langchain.prompts import PromptTemplate

planning_prompt = PromptTemplate(
    input_variables=["user_request", "schema"],
    template="""
    You are a technical documentation specialist tasked with creating comprehensive documents based on code analysis.
    
    User Request: {user_request}
    
    Available Graph Schema:
    {schema}
    
    Based on the user's request and the available graph schema, plan what information should be included in the document.
    
    Please provide a structured plan with:
    1. Document title
    2. Main sections to include
    3. Specific queries needed to gather information for each section
    4. The type of content for each section (overview, detailed analysis, examples, etc.)
    
    Format your response as JSON with the following structure:
    {{
        "title": "Document Title",
        "sections": [
            {{
                "section_name": "Section Name",
                "content_type": "overview|analysis|examples|reference",
                "queries": ["Query 1", "Query 2"],
                "description": "What this section will contain"
            }}
        ]
    }}
    """
)

content_prompt = PromptTemplate(
    input_variables=["section_name", "graph_data", "user_request"],
    template="""You are generating documentation content based on actual codebase data.

Section to generate: {section_name}
Codebase data from graph: {graph_data}
Original request: {user_request}

Generate comprehensive content for the {section_name} section using the provided codebase data.
Focus on:
- Real information from the codebase structure
- Practical examples based on the code
- Accurate technical details

Generate clear, well-structured markdown content."""
)

compilation_prompt = PromptTemplate(
    input_variables=["title", "sections", "user_request"],
    template="""
    Compile the following sections into a cohesive technical document.
    
    Original Request: {user_request}
    Document Title: {title}
    
    Sections:
    {sections}
    
    Create a final, well-formatted markdown document with:
    1. Title and table of contents
    2. Introduction explaining the document's purpose
    3. All sections properly organized
    4. Conclusion with key insights
    5. Proper markdown formatting throughout
    
    Make sure the document flows well and provides comprehensive coverage of the requested topic.
    """
)

generation_agent_prompt = PromptTemplate.from_template(
"""
You are an expert technical documentation generator. You can create comprehensive documentation by analyzing codebases stored in a Neo4j graph database.

You have access to the following tools:

{tools}

Your main goal is to help users generate high-quality technical documentation sections based on their requests.

IMPORTANT: 
- For specific queries about the codebase, use QueryCodebase
- For schema information, use GetSchemaInfo

Use the following format EXACTLY:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

IMPORTANT: You MUST end with "Final Answer:" followed by your response.

User input:{input}
{agent_scratchpad}
"""
)