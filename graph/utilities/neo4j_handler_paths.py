import json
from pathlib import Path
from neo4j import GraphDatabase
from .text_splitter import DocumentChunker

class CodeGraph:
    def __init__(self, uri, user, password, json_file):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        with open(json_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        # Initialize document chunker
        self.chunker = DocumentChunker(chunk_size=800, chunk_overlap=100)

    def close(self):
        self.driver.close()

    def clear_graph(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def build_graph(self):
        print(f"Starting to build graph with {len(self.data)} files...")
        
        with self.driver.session() as session:
            processed_count = 0
            chunked_files_count = 0
            total_chunks_created = 0
            
            for file_obj in self.data:
                try:
                    file_path = file_obj.get('file')
                    if not file_path:
                        continue

                    processed_count += 1
                    if processed_count % 50 == 0:
                        print(f"Processed {processed_count} files...")

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

                    # Handle files based on their type field from JSON
                    file_type = file_obj.get('type')
                    
                    if file_type == 'markdown':
                        content = file_obj.get('content', '')
                        session.run(
                            "MERGE (f:File {path: $file_path}) SET f:Markdown",
                            file_path=str(file_path)
                        )
                        if content and content.strip():
                            chunked_files_count += 1
                            chunk_ids = self._create_chunks_for_content(session, file_path, content, 'markdown')
                            total_chunks_created += len(chunk_ids)
                            if chunked_files_count <= 5:  # Log first few chunked files
                                print(f"Chunked markdown file {chunked_files_count}: {file_path} -> {len(chunk_ids)} chunks")
                            if chunk_ids:
                                for chunk_id in chunk_ids:
                                    session.run(
                                        "MATCH (f:File {path: $file_path}) "
                                        "MATCH (c:Chunk {id: $chunk_id}) "
                                        "MERGE (f)-[:CONTAINS]->(c)",
                                        file_path=str(file_path), chunk_id=chunk_id
                                    )
                    
                    elif file_type == 'text':
                        content = file_obj.get('content', '')
                        session.run(
                            "MERGE (f:File {path: $file_path}) SET f:TextFile",
                            file_path=str(file_path)
                        )
                        if content and content.strip():
                            chunked_files_count += 1
                            chunk_ids = self._create_chunks_for_content(session, file_path, content, 'text')
                            total_chunks_created += len(chunk_ids)
                            if chunked_files_count <= 5:  # Log first few chunked files
                                print(f"Chunked text file {chunked_files_count}: {file_path} -> {len(chunk_ids)} chunks")
                            if chunk_ids:
                                for chunk_id in chunk_ids:
                                    session.run(
                                        "MATCH (f:File {path: $file_path}) "
                                        "MATCH (c:Chunk {id: $chunk_id}) "
                                        "MERGE (f)-[:CONTAINS]->(c)",
                                        file_path=str(file_path), chunk_id=chunk_id
                                    )
                    
                    elif file_type == 'yaml':
                        content = json.dumps(file_obj.get('content', {}))
                        session.run(
                            "MERGE (f:File {path: $file_path}) SET f:YAML",
                            file_path=str(file_path)
                        )
                        if content and content.strip() and content != '{}':
                            chunk_ids = self._create_chunks_for_content(session, file_path, content, 'yaml')
                            if chunk_ids:
                                for chunk_id in chunk_ids:
                                    session.run(
                                        "MATCH (f:File {path: $file_path}) "
                                        "MATCH (c:Chunk {id: $chunk_id}) "
                                        "MERGE (f)-[:CONTAINS]->(c)",
                                        file_path=str(file_path), chunk_id=chunk_id
                                    )
                    
                    else:  # Python files and others
                        session.run(
                            "MERGE (f:File {path: $file_path})",
                            file_path=str(file_path)
                        )

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
                            # Method to method calls (same or different class)
                            session.run(
                                "MATCH (m:Method {name: $caller, class: $caller_class}) "
                                "MATCH (t:Method {name: $called}) "
                                "MERGE (m)-[:CALLS {caller_function: $caller, caller_class: $caller_class, called_function: $called}]->(t)",
                                caller=caller, caller_class=caller_class, called=called
                            )
                            # Method to function calls
                            session.run(
                                "MATCH (m:Method {name: $caller, class: $caller_class}) "
                                "MATCH (fn:Function {name: $called}) "
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

                    # Create USES relationships for external imports (simplified)
                    external_imports = [imp.get('module') for imp in file_obj.get('imports', []) if imp.get('type') == 'external']
                    if external_imports:
                        for module_name in external_imports[:5]:  # Limit to avoid too many relationships
                            if module_name:
                                session.run(
                                    "MERGE (lib:Library {name: $module_name}) "
                                    "WITH lib "
                                    "MATCH (f:File {path: $file_path}) "
                                    "MERGE (f)-[:USES]->(lib)",
                                    file_path=str(file_path), module_name=str(module_name)
                                )

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")
                    continue

            print(f"Graph build summary:")
            print(f"  Total files processed: {processed_count}")
            print(f"  Files with content chunks: {chunked_files_count}")
            print(f"  Total chunks created: {total_chunks_created}")

    def _create_chunks_for_content(self, session, source_id, content, content_type):
        """Create chunks for content and link them with FOLLOWS relationships
        Returns list of created chunk IDs"""
        print(f"_create_chunks_for_content called: source_id={source_id}, content_type={content_type}, content_length={len(content)}")
        
        if not content or not content.strip():
            print(f"No content to chunk for {source_id}")
            return []
        
        try:
            # Split content into chunks
            chunks = self.chunker.split_text(content)
            print(f"Text splitter created {len(chunks)} chunks for {source_id}")
            if not chunks:
                return []
                
            chunk_metadata = self.chunker.create_chunk_metadata(source_id, chunks)
            print(f"Created metadata for {len(chunk_metadata)} chunks")
            chunk_ids = []
            
            # Create all chunk nodes
            for i, chunk_data in enumerate(chunk_metadata):
                print(f"Creating chunk {i+1}/{len(chunk_metadata)}: {chunk_data['id']}")
                session.run("""
                    CREATE (c:Chunk {
                        id: $chunk_id,
                        content: $content,
                        chunk_index: $chunk_index,
                        total_chunks: $total_chunks,
                        source_id: $source_id,
                        content_type: $content_type,
                        char_count: $char_count,
                        word_count: $word_count
                    })
                """, {
                    "chunk_id": chunk_data["id"],
                    "content": chunk_data["content"],
                    "chunk_index": chunk_data["chunk_index"],
                    "total_chunks": chunk_data["total_chunks"],
                    "source_id": source_id,
                    "content_type": content_type,
                    "char_count": chunk_data["char_count"],
                    "word_count": chunk_data["word_count"]
                })
                chunk_ids.append(chunk_data["id"])
            
            print(f"Created {len(chunk_ids)} chunk nodes")
            
            # Create FOLLOWS relationships between consecutive chunks
            for i in range(1, len(chunk_metadata)):
                prev_chunk_id = chunk_metadata[i-1]["id"]
                curr_chunk_id = chunk_metadata[i]["id"]
                
                print(f"Creating FOLLOWS relationship: {prev_chunk_id} -> {curr_chunk_id}")
                session.run("""
                    MATCH (prev:Chunk {id: $prev_id})
                    MATCH (curr:Chunk {id: $curr_id})
                    MERGE (prev)-[:FOLLOWS]->(curr)
                """, {"prev_id": prev_chunk_id, "curr_id": curr_chunk_id})
            
            print(f"Created {len(chunk_metadata)-1} FOLLOWS relationships")
            return chunk_ids
                
        except Exception as e:
            print(f"Error creating chunks for {source_id}: {e}")
            import traceback
            traceback.print_exc()
            return []

