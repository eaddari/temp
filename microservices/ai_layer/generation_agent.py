import os
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from query_agent import agent_executor as query_agent, get_graph_schema, advanced_agent
from typing import Dict, Any
import json

load_dotenv()

llm = AzureChatOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    temperature=0.3
)

class DocumentGenerationAgent:
    def __init__(self, llm, query_agent):
        self.llm = llm
        self.query_agent = query_agent
        self.document_sections = []
        
        # Document planning prompt
        self.planning_prompt = PromptTemplate(
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
        
        self.content_prompt = PromptTemplate(
            input_variables=["section_info", "query_results", "user_request"],
            template="""
            You are writing a section for a technical document.
            
            Original User Request: {user_request}
            
            Section Information:
            - Name: {section_info}
            - Type: {content_type}
            - Description: {description}
            
            Query Results:
            {query_results}
            
            Write a comprehensive, well-structured section based on the query results. 
            Use proper markdown formatting, include code examples when relevant, and make it informative and readable.
            Focus on providing value to developers who need to understand this codebase.
            """
        )
        
        self.compilation_prompt = PromptTemplate(
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
    
    def plan_document(self, user_request: str) -> Dict[str, Any]:
        """Plan the document structure based on user request and available schema."""
        try:
            schema = get_graph_schema()
            
            planning_chain = self.planning_prompt | self.llm | StrOutputParser()
            plan_result = planning_chain.invoke({
                "user_request": user_request,
                "schema": schema
            })
            
            plan = json.loads(plan_result)
            return plan

        except json.JSONDecodeError:
            return {
                "title": f"Documentation for: {user_request}",
                "sections": [
                    {
                        "section_name": "Overview",
                        "content_type": "overview",
                        "queries": [f"What information is available related to: {user_request}"],
                        "description": "General overview of the requested topic"
                    }
                ]
            }
        except Exception as e:
            print(f"Error in planning: {e}")
            return {"title": "Error in Planning", "sections": []}
    
    def execute_queries(self, queries: list) -> str:
        """Execute a list of queries using the query agent."""
        results = []
        
        for query in queries:
            try:
                print(f"\n🔍 Executing query: {query}")
                response = self.query_agent.invoke({"input": query})
                results.append(f"Query: {query}\nResult: {response['output']}\n")
            except Exception as e:
                results.append(f"Query: {query}\nError: {str(e)}\n")
        
        return "\n".join(results)
    
    def generate_section(self, section_info: Dict[str, Any], user_request: str) -> str:
        """Generate content for a specific section."""
        queries = section_info.get("queries", [])
        query_results = self.execute_queries(queries)
        
        content_chain = self.content_prompt | self.llm | StrOutputParser()
        
        section_content = content_chain.invoke({
            "section_info": section_info["section_name"],
            "content_type": section_info.get("content_type", "overview"),
            "description": section_info.get("description", ""),
            "query_results": query_results,
            "user_request": user_request
        })
        
        return section_content
    
    def compile_document(self, title: str, sections: list, user_request: str) -> str:
        """Compile all sections into a final document."""
        sections_text = "\n\n".join(sections)
        
        compilation_chain = self.compilation_prompt | self.llm | StrOutputParser()
        
        final_document = compilation_chain.invoke({
            "title": title,
            "sections": sections_text,
            "user_request": user_request
        })
        
        return final_document
    
    def generate_document(self, user_request: str) -> str:
        """Main method to generate a complete document."""
        print(f"🚀 Starting document generation for: {user_request}")
        
        # Step 1: Plan the document
        print("📋 Planning document structure...")
        plan = self.plan_document(user_request)
        
        if not plan.get("sections"):
            return "Error: Could not create a valid document plan."
        
        print(f"📄 Document title: {plan['title']}")
        print(f"📝 Planned sections: {len(plan['sections'])}")
        
        generated_sections = []
        for i, section_info in enumerate(plan["sections"], 1):
            print(f"\n✍️  Generating section {i}/{len(plan['sections'])}: {section_info['section_name']}")
            section_content = self.generate_section(section_info, user_request)
            generated_sections.append(f"## {section_info['section_name']}\n\n{section_content}")
        
        print("\n📖 Compiling final document...")
        final_document = self.compile_document(plan["title"], generated_sections, user_request)
        
        return final_document

generation_agent = DocumentGenerationAgent(llm, query_agent)

def generate_documentation(request: str) -> str:
    """Generate comprehensive documentation based on the user's request."""
    try:
        result = generation_agent.generate_document(request)
        return result
    except Exception as e:
        return f"Error generating documentation: {str(e)}"

def query_codebase(query: str) -> str:
    """Query the codebase graph database for specific information."""
    try:
        response = query_agent.invoke({"input": query})
        return response["output"]
    except Exception as e:
        return f"Error querying codebase: {str(e)}"

def get_schema_info(input_str: str = "") -> str:
    """Get information about the available graph schema."""
    return get_graph_schema()

generation_tools = [
    Tool(
        name="GenerateDocumentation",
        func=generate_documentation,
        description="Generate comprehensive technical documentation based on user requirements. Use this for creating complete documents."
    ),
    Tool(
        name="QueryCodebase",
        func=query_codebase,
        description="Query the codebase graph database for specific information about classes, functions, relationships, etc."
    ),
    Tool(
        name="GetSchemaInfo",
        func=get_schema_info,
        description="Get information about the available graph database schema and what types of data can be queried."
    )
]

generation_agent_prompt = PromptTemplate.from_template(
"""
You are an expert technical documentation generator. You can create comprehensive documentation by analyzing codebases stored in a Neo4j graph database.

You have access to the following tools:

{tools}

Your main goal is to help users generate high-quality technical documentation based on their requests.

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

Question: {input}
{agent_scratchpad}
"""
)

generation_agent_executor = create_react_agent(llm, generation_tools, generation_agent_prompt)
generation_agent_runner = AgentExecutor(
    agent=generation_agent_executor,
    tools=generation_tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=15
)

if __name__ == "__main__":
    print("🤖 Document Generation Agent")
    print("=" * 50)
    
    print("\nEnter your documentation requests (type 'exit' to quit):")
    while True:
        try:
            user_input = input("\n📝 What documentation would you like me to generate? ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            print(f"\n🔄 Processing your request...")
            result = generation_agent.generate_document(user_input)
            
            print("\n" + "="*80)
            print("📄 GENERATED DOCUMENT")
            print("="*80)
            print(result)
            print("="*80)
            
            save = input("\n💾 Would you like to save this document to a file? (y/n): ")
            if save.lower() == 'y':
                filename = input("Enter filename (without extension): ")
                with open(f"{filename}.md", "w", encoding="utf-8") as f:
                    f.write(result)
                print(f"✅ Document saved as {filename}.md")
                
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")