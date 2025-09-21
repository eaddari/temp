import os
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from utilities.llm import llm
from query_agent.tools import tools
from query_agent.prompts import agent_prompt

load_dotenv(r"C:\desktopnoonedrive\docgenofficial\AIDocGen\.env", override=True)

agent = create_react_agent(llm, tools, agent_prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=False,
    handle_parsing_errors=True,
    max_iterations=10
)