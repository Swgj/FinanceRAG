from src.rag.data_to_milvus import load_nodes_to_milvus
from src.rag.document_parse import docs_parse, docs_parse_markdown
from llama_index.llms.ollama import Ollama
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.postprocessor.flag_embedding_reranker import FlagEmbeddingReranker
from llama_index.core import Settings
from src.config import config
import os

query_engine = None

def reranker_model(model_name_or_path):
    # here we use bge-reranker model
    bge_reranker = FlagEmbeddingReranker(
        top_n=5,
        model=model_name_or_path,
    )

    return bge_reranker


def get_query_engine():
    nodes = None
    if not os.path.exists(config.get('milvus')['uri']):
        md_files_dir = config.get_path('dataset', 'preprocessed_md')

        # Get knowledge base files
        md_files = []
        
        for root, dirs, files in os.walk(md_files_dir):
            for file in files:
                if file.endswith('.md'):
                    md_files.append(os.path.join(root, file))
        
        # Load nodes to Milvus
        # nodes = docs_parse(md_files)
        nodes = docs_parse_markdown(md_files)

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
    

    # Reranker model
    reranker = reranker_model(
        config.get_path('models', 'reranker')
    )

    # query_engine = index.as_chat_engine()
    query_engine = index.as_query_engine(
        similarity_top_k=5,
        node_postprocessors=[reranker],
        verbose=True
    )
    return query_engine

def query(query_text):
    global query_engine
    if query_engine is None:
        query_engine = get_query_engine()

    if not query_engine:
        return query_engine.query(query_text)
    else:
        return f"Query engine not initialized"

    