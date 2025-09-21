from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor


from planning_agent.tools import planning_tools, llm
from planning_agent.prompts import planning_agent_prompt

load_dotenv(r"C:\desktopnoonedrive\docgenofficial\AIDocGen\.env", override=True)

planning_agent_executor = create_react_agent(llm, planning_tools, planning_agent_prompt)


planning_agent_runner = AgentExecutor(
    agent=planning_agent_executor,
    tools=planning_tools,
    verbose=False,
    handle_parsing_errors=True,
    max_iterations=10
)

