import json
from pathlib import Path
from neo4j import GraphDatabase

class CodeGraph:
    def __init__(self, uri, user, password, json_file):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        with open(json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def close(self):
        self.driver.close()

    def clear_graph(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def build_graph(self):
        with self.driver.session() as session:
            for file_obj in self.data:
                file_path = file_obj.get('file')
                if not file_path:
                    continue
                # File node
                session.run(
                    "MERGE (f:File {path: $file_path})",
                    file_path=str(file_path)
                )
                folder_path = str(Path(file_path).parent)
                session.run(
                    "MERGE (d:Folder {path: $folder_path})",
                    folder_path=folder_path
                )
                session.run(
                    "MATCH (f:File {path: $file_path}), (d:Folder {path: $folder_path}) "
                    "MERGE (d)-[:CONTAINS]->(f)",
                    file_path=str(file_path), folder_path=folder_path
                )
                current_folder = folder_path
                while True:
                    parent_folder = str(Path(current_folder).parent)
                    if parent_folder == current_folder or parent_folder in ('.', ''):
                        break
                    session.run(
                        "MERGE (p:Folder {path: $parent_folder})",
                        parent_folder=parent_folder
                    )
                    session.run(
                        "MATCH (p:Folder {path: $parent_folder}), (c:Folder {path: $current_folder}) "
                        "MERGE (p)-[:CONTAINS]->(c)",
                        parent_folder=parent_folder, current_folder=current_folder
                    )
                    current_folder = parent_folder

                # Classes
                for cls in file_obj.get('classes', []):
                    class_name = cls.get('name')
                    if not class_name:
                        continue
                    session.run(
                        "MERGE (c:Class {name: $class_name, decorators: $decorators, inheritances: $inheritances})",
                        class_name=class_name,
                        decorators=json.dumps(cls.get('decorators', [])),
                        inheritances=json.dumps(cls.get('inheritances', []))
                    )
                    session.run(
                        "MATCH (f:File {path: $file_path}), (c:Class {name: $class_name}) "
                        "MERGE (f)-[:DEFINES]->(c)",
                        file_path=str(file_path), class_name=class_name
                    )
                    for method in cls.get('methods', []):
                        method_name = method.get('name')
                        if not method_name:
                            continue
                        session.run(
                            "MERGE (m:Method {name: $method_name, class: $class_name, content: $content, signature: $signature, decorators: $decorators})",
                            method_name=method_name,
                            class_name=class_name,
                            content=method.get('content', ''),
                            signature=json.dumps(method.get('signature', {})),
                            decorators=json.dumps(method.get('decorators', []))
                        )
                        session.run(
                            "MATCH (c:Class {name: $class_name}), (m:Method {name: $method_name, class: $class_name}) "
                            "MERGE (c)-[:DEFINES]->(m)",
                            class_name=class_name, method_name=method_name
                        )

                # Functions
                for func in file_obj.get('functions', []):
                    function_name = func.get('name')
                    if not function_name:
                        continue
                    session.run(
                        "MERGE (fn:Function {name: $function_name, content: $content, signature: $signature, decorators: $decorators})",
                        function_name=function_name,
                        content=func.get('content', ''),
                        signature=json.dumps(func.get('signature', {})),
                        decorators=json.dumps(func.get('decorators', []))
                    )
                    session.run(
                        "MATCH (f:File {path: $file_path}), (fn:Function {name: $function_name}) "
                        "MERGE (f)-[:DEFINES]->(fn)",
                        file_path=str(file_path), function_name=function_name
                    )

                # Calls
                for call in file_obj.get('calls', []):
                    caller = call.get('caller_function')
                    caller_class = call.get('caller_class')
                    called = call.get('called_function')
                    if not caller or not called:
                        continue
                    if caller_class:
                        session.run(
                            "MATCH (m:Method {name: $caller, class: $caller_class}), (t:Method {name: $called, class: $caller_class}) "
                            "MERGE (m)-[:CALLS {caller_function: $caller, caller_class: $caller_class, called_function: $called}]->(t)",
                            caller=caller, caller_class=caller_class, called=called
                        )
                        session.run(
                            "MATCH (m:Method {name: $caller, class: $caller_class}), (fn:Function {name: $called}) "
                            "MERGE (m)-[:CALLS {caller_function: $caller, caller_class: $caller_class, called_function: $called}]->(fn)",
                            caller=caller, caller_class=caller_class, called=called
                        )
                    else:
                        session.run(
                            "MATCH (fn:Function {name: $caller}), (t:Function {name: $called}) "
                            "MERGE (fn)-[:CALLS {caller_function: $caller, called_function: $called}]->(t)",
                            caller=caller, called=called
                        )
                        session.run(
                            "MATCH (fn:Function {name: $caller}), (m:Method {name: $called}) "
                            "MERGE (fn)-[:CALLS {caller_function: $caller, called_function: $called}]->(m)",
                            caller=caller, called=called
                        )

