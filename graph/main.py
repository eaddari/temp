import os
from utilities.neo4j_handler_paths import CodeGraph
from utilities.ast_to_json_parser import parse_parquet_to_json

JSON_FILE = '/app/data/input.json'
PARQUET_FILE_NAME = os.getenv("PARQUET_FILE_NAME", "output.parquet")
PARQUET_FILE_PATH = f'/app/outputs/{PARQUET_FILE_NAME}'
print("Starting graph builder...")
print(f"Converting {PARQUET_FILE_NAME} to JSON...")

parse_parquet_to_json(PARQUET_FILE_PATH, JSON_FILE, cross_calls=True)
print("Conversion completed.")

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "docgentest")

builder = CodeGraph(
    json_file=JSON_FILE,
    uri=NEO4J_URI,
    user=NEO4J_USER,
    password=NEO4J_PASSWORD
)

builder.clear_graph()
builder.build_graph()
print("Graph build completed!")
