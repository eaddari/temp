from graph.utilities.neo4j_handler_paths import CodeGraph

builder = CodeGraph(
    json_file="C:\\desktopnoonedrive\\docgenofficial\\AIDocGen\\repo_output.json",
    uri="bolt://localhost:7687",
    user="neo4j",
    password="docgentest"
)
builder.clear_graph()
builder.build_graph()
