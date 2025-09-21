# microservices.ai_layer.planning_agent

Source file: `microservices\ai_layer\planning_agent.py`

## Source Code

```python
import os
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from query_agent import get_graph_schema
from typing import Dict, Any, List
import json
import re

load_dotenv()

llm = AzureChatOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    temperature=0.1
)

class DocumentationPlanningAgent:
    def __init__(self, llm):
        self.llm = llm
        
        self.analysis_prompt = PromptTemplate(
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
        
        # Planning prompt
        self.planning_prompt = PromptTemplate(
            input_variables=["analysis", "user_request", "schema"],
            template="""
            Based on the analysis below, create a detailed documentation plan.
            
            Analysis: {analysis}
            Original Request: {user_request}
            Available Schema: {schema}
            
            Create a comprehensive plan with the following structure:
            
            {{
                "document_info": {{
                    "title": "Clear, descriptive title",
                    "type": "API documentation|Architecture guide|User manual|Reference|Overview",
                    "audience": "Primary target audience",
                    "estimated_length": "Short|Medium|Long",
                    "complexity": "Basic|Intermediate|Advanced"
                }},
                "sections": [
                    {{
                        "section_name": "Section Title",
                        "priority": "High|Medium|Low",
                        "content_type": "overview|detailed_analysis|code_examples|reference|tutorial",
                        "queries": [
                            "Specific query 1 to get needed data",
                            "Specific query 2 to get needed data"
                        ],
                        "description": "What this section will contain and why it's important",
                        "expected_content": "Brief description of expected content format"
                    }}
                ],
                "dependencies": [
                    {{
                        "section": "Section name that depends on another",
                        "depends_on": "Section it depends on",
                        "reason": "Why this dependency exists"
                    }}
                ],
                "quality_criteria": [
                    "Specific criteria for evaluating this documentation",
                    "What makes this documentation successful"
                ]
            }}
            
            Make sure queries are specific and actionable based on the available schema.
            Focus on creating a logical flow and comprehensive coverage.
            """
        )
        
        # Query optimization prompt
        self.query_optimization_prompt = PromptTemplate(
            input_variables=["queries", "schema", "context"],
            template="""
            You are a Neo4j Cypher query expert. Optimize these queries for efficiency and accuracy.
            
            Original Queries: {queries}
            Available Schema: {schema}
            Context: {context}
            
            For each query, provide:
            1. Optimized natural language query
            2. Expected result type
            3. Potential issues or limitations
            4. Alternative query approaches if needed
            
            Return as JSON:
            {{
                "optimized_queries": [
                    {{
                        "original": "Original query",
                        "optimized": "Improved natural language query",
                        "expected_result": "What type of data this should return",
                        "notes": "Any important considerations"
                    }}
                ]
            }}
            """
        )
    
    def analyze_request(self, user_request: str) -> str:
        """Analyze the user request to understand requirements."""
        try:
            schema = get_graph_schema()
            
            analysis_chain = self.analysis_prompt | self.llm | StrOutputParser()
            analysis = analysis_chain.invoke({
                "user_request": user_request,
                "schema": schema
            })
            
            return analysis
            
        except Exception as e:
            return f"Error analyzing request: {str(e)}"
    
    def create_documentation_plan(self, user_request: str, analysis: str = None) -> Dict[str, Any]:
        """Create a detailed documentation plan based on analysis."""
        try:
            if not analysis:
                analysis = self.analyze_request(user_request)
            
            schema = get_graph_schema()
            
            planning_chain = self.planning_prompt | self.llm | StrOutputParser()
            plan_result = planning_chain.invoke({
                "analysis": analysis,
                "user_request": user_request,
                "schema": schema
            })
            
            # Clean up the JSON response
            plan_result = self._clean_json_response(plan_result)
            
            try:
                plan = json.loads(plan_result)
                return plan
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw response: {plan_result[:500]}...")
                return self._create_fallback_plan(user_request)
            
        except Exception as e:
            print(f"Error creating plan: {e}")
            return self._create_fallback_plan(user_request)
    
    def optimize_queries(self, queries: List[str], context: str) -> List[Dict[str, str]]:
        """Optimize queries for better performance and accuracy."""
        try:
            schema = get_graph_schema()
            
            optimization_chain = self.query_optimization_prompt | self.llm | StrOutputParser()
            result = optimization_chain.invoke({
                "queries": queries,
                "schema": schema,
                "context": context
            })
            
            result = self._clean_json_response(result)
            optimized = json.loads(result)
            
            return optimized.get("optimized_queries", [])
            
        except Exception as e:
            print(f"Error optimizing queries: {e}")
            # Return original queries as fallback
            return [{"original": q, "optimized": q, "expected_result": "Data", "notes": "No optimization applied"} for q in queries]
    
    def validate_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and improve the documentation plan."""
        validation_results = {
            "is_valid": True,
            "issues": [],
            "suggestions": [],
            "improved_plan": plan
        }
        
        # Check for required fields
        required_fields = ["document_info", "sections"]
        for field in required_fields:
            if field not in plan:
                validation_results["is_valid"] = False
                validation_results["issues"].append(f"Missing required field: {field}")
        
        # Validate sections
        if "sections" in plan:
            for i, section in enumerate(plan["sections"]):
                if "section_name" not in section:
                    validation_results["issues"].append(f"Section {i+1} missing name")
                if "queries" not in section or not section["queries"]:
                    validation_results["suggestions"].append(f"Section '{section.get('section_name', f'Section {i+1}')}' has no queries")
        
        # Check for logical flow
        if len(plan.get("sections", [])) > 1:
            high_priority_sections = [s for s in plan["sections"] if s.get("priority") == "High"]
            if not high_priority_sections:
                validation_results["suggestions"].append("Consider marking at least one section as high priority")
        
        return validation_results
    
    def _clean_json_response(self, response: str) -> str:
        """Clean LLM response to extract valid JSON."""
        # Remove markdown code blocks
        response = re.sub(r'```json\s*', '', response)
        response = re.sub(r'```\s*$', '', response)
        
        # Find JSON content between braces
        start = response.find('{')
        end = response.rfind('}') + 1
        
        if start != -1 and end > start:
            return response[start:end]
        
        return response.strip()
    
    def _create_fallback_plan(self, user_request: str) -> Dict[str, Any]:
        """Create a basic fallback plan when automated planning fails."""
        return {
            "document_info": {
                "title": f"Documentation for: {user_request}",
                "type": "General documentation",
                "audience": "Developers",
                "estimated_length": "Medium",
                "complexity": "Intermediate"
            },
            "sections": [
                {
                    "section_name": "Overview",
                    "priority": "High",
                    "content_type": "overview",
                    "queries": [f"What is available related to: {user_request}"],
                    "description": "General overview of the requested topic",
                    "expected_content": "High-level description and context"
                },
                {
                    "section_name": "Detailed Analysis",
                    "priority": "Medium",
                    "content_type": "detailed_analysis",
                    "queries": [f"Show detailed information about: {user_request}"],
                    "description": "In-depth analysis of the topic",
                    "expected_content": "Detailed technical information"
                }
            ],
            "dependencies": [],
            "quality_criteria": [
                "Comprehensive coverage of the topic",
                "Clear and understandable explanations",
                "Accurate technical information"
            ]
        }

# Initialize the planning agent
planning_agent = DocumentationPlanningAgent(llm)

# Tool functions
def analyze_documentation_request(request: str) -> str:
    """Analyze a documentation request to understand requirements and scope."""
    try:
        analysis = planning_agent.analyze_request(request)
        return analysis
    except Exception as e:
        return f"Error analyzing request: {str(e)}"

def create_documentation_plan(request: str) -> str:
    """Create a detailed plan for generating documentation based on the request."""
    try:
        plan = planning_agent.create_documentation_plan(request)
        return json.dumps(plan, indent=2)
    except Exception as e:
        return f"Error creating plan: {str(e)}"

def validate_documentation_plan(plan_json: str) -> str:
    """Validate a documentation plan and provide improvement suggestions."""
    try:
        plan = json.loads(plan_json)
        validation = planning_agent.validate_plan(plan)
        return json.dumps(validation, indent=2)
    except Exception as e:
        return f"Error validating plan: {str(e)}"

def get_schema_information(input_str: str = "") -> str:
    """Get information about the available graph schema."""
    return get_graph_schema()

# Define tools for the planning agent
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

# Agent prompt for the planning agent
planning_agent_prompt = PromptTemplate.from_template(
"""
You are an expert documentation planning specialist. Your role is to analyze user requests and create comprehensive plans for technical documentation.

You excel at:
- Understanding complex documentation requirements
- Breaking down requests into actionable components
- Creating logical document structures
- Identifying the right queries to gather needed information
- Ensuring comprehensive coverage of topics

You have access to the following tools:

{tools}

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

# Create the planning agent executor
planning_agent_executor = create_react_agent(llm, planning_tools, planning_agent_prompt)
planning_agent_runner = AgentExecutor(
    agent=planning_agent_executor,
    tools=planning_tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10
)

if __name__ == "__main__":
    print("📋 Documentation Planning Agent")
    print("=" * 50)
    
    # Test the planning agent
    test_requests = [
        "Create API documentation for all the classes in the codebase",
        "Generate an architecture overview showing how different components interact",
        "Document the main functions and their usage patterns"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n🧪 Test {i}: {request}")
        print("-" * 40)
        
        try:
            # Test analysis
            print("\n📊 Analysis:")
            analysis = planning_agent.analyze_request(request)
            print(analysis[:300] + "..." if len(analysis) > 300 else analysis)
            
            # Test planning
            print("\n📋 Plan:")
            plan = planning_agent.create_documentation_plan(request)
            
            # Print a summary of the plan
            if plan and "document_info" in plan:
                info = plan["document_info"]
                print(f"Title: {info.get('title', 'N/A')}")
                print(f"Type: {info.get('type', 'N/A')}")
                print(f"Sections: {len(plan.get('sections', []))}")
                
                for j, section in enumerate(plan.get('sections', []), 1):
                    print(f"  {j}. {section.get('section_name', 'Unnamed Section')} ({section.get('priority', 'Medium')} priority)")
            
            # Test validation
            validation = planning_agent.validate_plan(plan)
            if not validation["is_valid"]:
                print(f"\n⚠️  Validation Issues: {len(validation['issues'])}")
            if validation["suggestions"]:
                print(f"💡 Suggestions: {len(validation['suggestions'])}")
                
        except Exception as e:
            print(f"❌ Error in test {i}: {e}")
    
    # Interactive mode
    print("\n" + "="*50)
    print("Interactive Mode - Enter documentation requests (type 'exit' to quit):")
    
    while True:
        try:
            user_input = input("\n📝 What documentation would you like me to plan? ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            print(f"\n🔄 Analyzing and planning...")
            
            # Create comprehensive plan
            plan = planning_agent.create_documentation_plan(user_input)
            
            print("\n" + "="*60)
            print("📋 DOCUMENTATION PLAN")
            print("="*60)
            
            if plan and "document_info" in plan:
                info = plan["document_info"]
                print(f"📄 Title: {info.get('title', 'N/A')}")
                print(f"🎯 Type: {info.get('type', 'N/A')}")
                print(f"👥 Audience: {info.get('audience', 'N/A')}")
                print(f"📏 Length: {info.get('estimated_length', 'N/A')}")
                print(f"🔧 Complexity: {info.get('complexity', 'N/A')}")
                
                print(f"\n📑 Sections ({len(plan.get('sections', []))}):")
                for j, section in enumerate(plan.get('sections', []), 1):
                    priority_emoji = "🔴" if section.get('priority') == 'High' else "🟡" if section.get('priority') == 'Medium' else "🟢"
                    print(f"  {priority_emoji} {j}. {section.get('section_name', 'Unnamed Section')}")
                    print(f"     Type: {section.get('content_type', 'N/A')}")
                    print(f"     Queries: {len(section.get('queries', []))}")
                    print(f"     Description: {section.get('description', 'N/A')[:100]}...")
                
                if plan.get('dependencies'):
                    print(f"\n🔗 Dependencies ({len(plan['dependencies'])}):")
                    for dep in plan['dependencies']:
                        print(f"  • {dep.get('section', 'N/A')} depends on {dep.get('depends_on', 'N/A')}")
                
                if plan.get('quality_criteria'):
                    print(f"\n✅ Quality Criteria:")
                    for criterion in plan['quality_criteria']:
                        print(f"  • {criterion}")
            
            print("="*60)
            
            # Validate the plan
            validation = planning_agent.validate_plan(plan)
            if not validation["is_valid"] or validation["suggestions"]:
                print("\n🔍 Validation Results:")
                if validation["issues"]:
                    print("❌ Issues:")
                    for issue in validation["issues"]:
                        print(f"  • {issue}")
                if validation["suggestions"]:
                    print("💡 Suggestions:")
                    for suggestion in validation["suggestions"]:
                        print(f"  • {suggestion}")
            else:
                print("\n✅ Plan validation passed!")
                
        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

```
