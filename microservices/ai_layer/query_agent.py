import os
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_community.graphs import Neo4jGraph
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate

load_dotenv()

# Initialize Neo4j connection
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD")
)

llm = AzureChatOpenAI(
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
    temperature=0
)

# Advanced Neo4j Agent Class
class AdvancedNeo4jAgent:
    def __init__(self, graph, llm):
        self.graph = graph
        self.llm = llm
        self.cypher_prompt = PromptTemplate(
            input_variables=["schema", "question"],
            template="""
            Task: Generate Cypher statement to query a graph database.
            Instructions:
            Use only the provided relationship types and properties in the schema.
            Do not use any other relationship types or properties that are not provided.
            
            Schema:
            {schema}
            
            Note: Do not include any explanations or apologies in your responses.
            Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
            Do not include any text except the generated Cypher statement.
            
            Question: {question}
            """
        )
        
        self.cypher_chain = self.cypher_prompt | llm
    
    def query(self, question: str):
        """Generate and execute Cypher query based on natural language question."""
        # Generate Cypher query
        cypher_query = self.cypher_chain.invoke({
            "schema": self.graph.schema,
            "question": question
        })
        
        # Use the query directly without correction for now
        corrected_query = cypher_query.content.strip()
        
        try:
            # Execute the query
            result = self.graph.query(corrected_query)
            return {
                "query": corrected_query,
                "result": result,
                "success": True
            }
        except Exception as e:
            return {
                "query": corrected_query,
                "error": str(e),
                "success": False
            }

# Initialize advanced agent
advanced_agent = AdvancedNeo4jAgent(graph, llm)

# Standard cypher chain for fallback
cypher_chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    return_intermediate_steps=True,
    allow_dangerous_requests=True
)

def query_graph(query: str) -> str:
    """Query the Neo4j graph database using natural language."""
    try:
        result = cypher_chain.run(query)
        return result
    except Exception as e:
        return f"Error querying graph: {str(e)}"

def query_graph_advanced(query: str) -> str:
    """Query the Neo4j graph database using advanced natural language processing."""
    try:
        result = advanced_agent.query(query)
        if result["success"]:
            return f"Query executed successfully:\nCypher: {result['query']}\nResult: {result['result']}"
        else:
            fallback_result = cypher_chain.run(query)
            return f"Advanced query failed, used fallback:\nResult: {fallback_result}"
    except Exception as e:
        return f"Error querying graph: {str(e)}"

def get_graph_schema(input_str: str = "") -> str:
    """Get the schema of the Neo4j graph database."""
    return graph.schema

tools = [
    Tool(
        name="GraphQuery",
        func=query_graph,
        description="Use this tool to query the Neo4j graph database with natural language questions."
    ),
    Tool(
        name="GraphQueryAdvanced",
        func=query_graph_advanced,
        description="Use this tool for advanced querying of the Neo4j graph database with better Cypher generation and error handling."
    ),
    Tool(
        name="GraphSchema",
        func=get_graph_schema,
        description="Use this tool to get information about the graph database schema including node types and relationships."
    )
]

agent_prompt = PromptTemplate.from_template(
"""
You are a helpful assistant that can query a Neo4j property graph database.
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

IMPORTANT: You MUST end with "Final Answer:" followed by your response. Do not provide conversational responses without the "Final Answer:" prefix.

Question: {input}
{agent_scratchpad}
"""
)

# Create and run agent
agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=10
)

if __name__ == "__main__":
    print("Testing Neo4j Graph Agent with Advanced Capabilities")
    print("=" * 50)
    
    # Test schema retrieval
    print("\n1. Getting graph schema...")
    try:
        schema = get_graph_schema()
        print(f"Schema: {schema}")
    except Exception as e:
        print(f"Error getting schema: {e}")
    
    # Test basic query
    print("\n2. Testing basic query...")
    response = agent_executor.invoke({
        "input": "What types of nodes exist in the graph?"
    })
    print(f"Response: {response['output']}")
    
    # Test advanced query directly
    print("\n3. Testing advanced agent directly...")
    try:
        advanced_result = advanced_agent.query("Show me the first 5 nodes in the graph")
        if advanced_result["success"]:
            print(f"Advanced Query Success:")
            print(f"Cypher: {advanced_result['query']}")
            print(f"Result: {advanced_result['result']}")
        else:
            print(f"Advanced Query Failed: {advanced_result['error']}")
    except Exception as e:
        print(f"Error with advanced agent: {e}")
    
    # Interactive mode
    print("\n4. Starting interactive mode...")
    print("Enter your questions (type 'exit' to quit):")
    while True:
        try:
            user_input = input("\nYour question: ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            response = agent_executor.invoke({"input": user_input})
            print(f"Answer: {response['output']}")
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")