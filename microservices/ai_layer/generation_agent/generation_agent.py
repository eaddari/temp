import os
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor

from generation_agent.tools import tools, llm
from generation_agent.prompts import generation_agent_prompt

load_dotenv(r"C:\desktopnoonedrive\docgenofficial\AIDocGen\.env", override=True)

generation_agent_executor = create_react_agent(llm, tools, generation_agent_prompt)
generation_agent_runner = AgentExecutor(
    agent=generation_agent_executor,
    tools=tools,
    verbose=False,
    handle_parsing_errors=True,
    max_iterations=10
)