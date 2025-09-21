from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List


class DocumentChunker:
    """Minimal text splitter using langchain for chunking documents before Neo4j upload"""
    
    def __init__(self, chunk_size: int = 800, chunk_overlap: int = 100):
        """Initialize with langchain text splitter"""
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def split_text(self, text: str) -> List[str]:
        """Split text into chunks using langchain splitter"""
        return self.text_splitter.split_text(text)
    
    def create_chunk_metadata(self, file_path: str, chunks: List[str]) -> List[dict]:
        """Create chunk metadata for Neo4j nodes"""
        chunk_data = []
        for i, chunk_text in enumerate(chunks):
            chunk_data.append({
                "id": f"{file_path}_chunk_{i}",
                "content": chunk_text,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "source_file": file_path,
                "char_count": len(chunk_text),
                "word_count": len(chunk_text.split())
            })
        return chunk_data


def chunk_document(file_path: str, content: str, chunk_size: int = 800) -> List[dict]:
    """Convenience function to chunk a document and return metadata"""
    chunker = DocumentChunker(chunk_size=chunk_size)
    chunks = chunker.split_text(content)
    return chunker.create_chunk_metadata(file_path, chunks)
