import os
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor

from quality_agent.tools import tools, llm
from quality_agent.prompts import quality_agent_prompt

load_dotenv(r"C:\desktopnoonedrive\docgenofficial\AIDocGen\.env", override=True)

quality_agent_executor = create_react_agent(llm, tools, quality_agent_prompt)
quality_agent_runner = AgentExecutor(
    agent=quality_agent_executor,
    tools=tools,
    verbose=False,
    handle_parsing_errors=True,
    max_iterations=5
)
