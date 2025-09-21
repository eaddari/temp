import os
from langchain.tools import Tool
from langchain_openai import AzureChatOpenAI
from langchain_neo4j import Neo4jGraph
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from query_agent.prompts import cypher_prompt
from dotenv import load_dotenv
from utilities.llm import llm
load_dotenv()

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD")
)


def query_neo4j(question: str) -> str:
    try:
        schema = graph.schema
        chain = cypher_prompt | llm | StrOutputParser()
        cypher = chain.invoke({"schema": schema, "question": question})
        cypher = cypher.strip().replace('```', '').replace('cypher', '')
        result = graph.query(cypher)
        return str(result) if result else "No results found"
    except Exception:
        return "Query failed"

def get_graph_schema(input_text=""):
    return graph.schema

tools = [
    Tool(
        name="QueryNeo4j",
        func=query_neo4j,
        description="Query the Neo4j graph database"
    ),
    Tool(
        name="GetSchema",
        func=get_graph_schema,
        description="Get database schema"
    )
]