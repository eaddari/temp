from langchain.prompts import PromptTemplate

planning_agent_prompt = PromptTemplate.from_template(
"""
You are a documentation planning agent. Your role is to analyze user requests and create comprehensive documentation plans.

You have access to the following tools:
{tools}

Use this format EXACTLY:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: {{
    "title": "Documentation Title",
    "description": "Brief description", 
    "estimated_length": "Short|Medium|Long",
    "sections": [
        {{
            "section_name": "Section Name",
            "content_type": "content type", 
            "priority": "priority level",
            "description": "section description"
        }}
    ]
}}

Your workflow should typically be:
1. Use AnalyzeRequest to understand the user's needs
2. Use GetSchemaInfo to understand available data
3. Use CreatePlan to generate a documentation plan
4. Use ValidatePlan to ensure the plan is complete and valid

Question: {input}
{agent_scratchpad}
"""
)

analysis_prompt = PromptTemplate(
            input_variables=["user_request", "schema"],
            template="""
            You are an expert technical documentation analyst. Your job is to understand user requests and break them down into actionable components.
            
            User Request: {user_request}
            
            Available Graph Schema (what data is available):
            {schema}
            
            Analyze this request and provide:
            1. Document type classification (API docs, architecture overview, user guide, reference manual, etc.)
            2. Target audience (developers, architects, end-users, etc.)
            3. Scope and complexity level
            4. Key topics that should be covered
            5. Required data types from the graph (classes, functions, relationships, etc.)
            6. Estimated documentation sections needed
            
            Provide your analysis in a structured format focusing on what information is needed and available.
            """
        )

planning_prompt = PromptTemplate(
            input_variables=["analysis", "user_request", "schema"],
            template="""
            Based on the analysis below, create a detailed documentation plan.
            
            Analysis: {analysis}
            Original Request: {user_request}
            Available Schema: {schema}
            
            Create a comprehensive plan that includes:
            - A descriptive title for the documentation
            - A brief description of what the documentation will cover
            - An estimated length (Short, Medium, or Long)
            - A list of sections with their details
            
            For each section, include:
            - section_name: Clear, descriptive name
            - content_type: Type of content (overview, analysis, examples, reference, tutorial)
            - priority: Importance level (High, Medium, Low)
            - description: What this section will contain
            
            Present your plan as a JSON object with the structure:
            {{
                "title": "Documentation Title",
                "description": "Brief description",
                "estimated_length": "Short|Medium|Long",
                "sections": [
                    {{
                        "section_name": "Section Name",
                        "content_type": "content type",
                        "priority": "priority level",
                        "description": "section description"
                    }}
                ]
            }}
            """
        )

readme_planning_prompt = PromptTemplate(
            input_variables=["analysis", "user_request", "schema"],
            template="""
            Based on the analysis below, create a detailed README plan.

            Analysis: {analysis}
            Original Request: {user_request}
            Available Schema: {schema}

            Use the following JSON structure to create the plan, which should have at least the most important sections:
            
            {{
                "title": "Project Title (descriptive name for the software)",
                "description": "Brief one-sentence summary of the software's purpose and functionality",
                "estimated_length": "Medium",
                "sections": [
                    {{
                        "section_name": "General Information",
                        "content_type": "overview",
                        "priority": "High",
                        "description": "Project name, version using semantic versioning, and short description of software's purpose and functionality"
                    }},
                    {{
                        "section_name": "Project Overview", 
                        "content_type": "overview",
                        "priority": "High",
                        "description": "Full description of software's purpose and notable features, date of creation, project organization details, and software project size"
                    }},
                    {{
                        "section_name": "Installation",
                        "content_type": "tutorial", 
                        "priority": "High",
                        "description": "Step-by-step installation instructions, system requirements, required libraries and dependencies, setup requirements, and known installation issues"
                    }},
                    {{
                        "section_name": "Usage",
                        "content_type": "examples",
                        "priority": "High", 
                        "description": "Instructions for running the software with expected output, usage examples, screenshots where appropriate, testing instructions, and known limitations"
                    }},
                    {{
                        "section_name": "License",
                        "content_type": "reference",
                        "priority": "Medium",
                        "description": "Software license information, restrictions on use, and preferred citation format for publications"
                    }},
                    {{
                        "section_name": "Contact Information",
                        "content_type": "reference", 
                        "priority": "Low",
                        "description": "Contact details for maintainers and contributors including name, role, ORCID, institution, and email"
                    }},
                    {{
                        "section_name": "Acknowledgements",
                        "content_type": "reference",
                        "priority": "Low", 
                        "description": "Funding sources with grant numbers, related publications, project availability locations, relationships to other projects, and complete contributor list"
                    }}
                ]
            }}
            """
        )
