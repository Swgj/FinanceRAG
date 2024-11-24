from src.rag.data_to_milvus import load_nodes_to_milvus
from src.rag.document_parse import docs_parse
from llama_index.llms.ollama import Ollama
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.core import Settings
from src.config import config
import os

query_engine = None

def get_query_engine():
    nodes = None
    if not os.path.exists(config.get('milvus')['uri']):
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
    if config.get("llm") == "huggingface":
        Settings.llm = HuggingFaceLLM(
            model_name=config.get_path('models', 'rag'),
            tokenizer_name=config.get_path('models', 'rag'),
            )
    elif config.get("llm") == "ollama":
        Settings.llm = Ollama(model=config.get('models')['rag']) # do not change get to get_path, here's getting name
    else:
        raise Exception("Invalid LLM")
    
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

    