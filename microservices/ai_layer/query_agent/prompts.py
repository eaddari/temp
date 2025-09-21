from langchain.prompts import PromptTemplate

cypher_prompt = PromptTemplate(
input_variables=["schema", "question"],
template="""
Task: Generate a Cypher statement to query a graph database.

Formulate the queries in a practical and efficient manner, for example:
If the context of action is broad, about project overviews, folder structure  or project structures, focus on nodes like Folders and Files. Do not focus on specific code details.
If the context of action is about specific code details, focus on nodes like Classes, Functions, Methods, Variables, and their relationships. Do not focus on high-level project structure.
Don't specifically look for the section names in the nodes' content, as they might not be explicitly mentioned. Instead, infer them from the graph structure and relationships.
Instructions:
- Use only the provided relationship types and properties in the schema
- Use modern Neo4j syntax: for example "property IS NOT NULL" instead of "exists(property)"
- Follow proper Cypher clause order: MATCH, WHERE, RETURN (never start with WHERE)
- WHERE clauses must always follow MATCH clauses
- Add LIMIT clause (max 50 results unless counting)
- Use specific node labels and properties when possible
- Keep queries concise and efficient
- If using UNION, ensure all parts return the same column names and types
- Prefer simple MATCH patterns over complex unions when possible
- Avoid UNION unless absolutely necessary for the query

Schema:
{schema}

Question: {question}

Cypher statement:
"""
        )

agent_prompt = PromptTemplate.from_template(
"""
You are a helpful assistant that can query a Neo4j graph database to find information about code repositories.

Available tools:
{tools}

Please follow this format:

Question: the input question you must answer
Thought: think about what information you need from the database
Thought: consider that for some informations it's not necessary to specifically look for it in the nodes' content.
Thought: information can be inferred from the graph structure and node relationships.
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat as needed)
Thought: I now have the information needed
Final Answer: provide a comprehensive answer based on the data retrieved

Question: {input}
{agent_scratchpad}
"""
)