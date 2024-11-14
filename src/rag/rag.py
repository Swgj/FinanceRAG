from src.rag.data_to_milvus import load_nodes_to_milvus
from rag.document_parse import docs_parse
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from src.config import config
import os

query_engine = None

def get_query_engine():
    # Get knowledge base files
    md_files = []
    md_files_dir = config.get_path('dataset', 'preprocessed_md')
    for root, dirs, files in os.walk(md_files_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    
    # Load nodes to Milvus
    nodes = docs_parse(md_files)
    index = load_nodes_to_milvus(nodes)

    # Query engine
    Settings.llm = Ollama(model=config.get('models')['rag'])
    query_engine = index.as_chat_engine()

    return query_engine

def query(query_text):
    global query_engine
    if query_engine is None:
        query_engine = get_query_engine()

    if not query_engine:
        return query_engine.query(query_text)
    else:
        return f"Query engine not initialized"

    