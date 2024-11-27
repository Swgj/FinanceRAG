from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.milvus import MilvusVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from src.utils.torch_utils import get_device
from src.config import config
import os

def embedding_model(model_name_or_path):
    # here we use bge-embedding model
    bge_embedding = HuggingFaceEmbedding(
        model_name=model_name_or_path,
        device=get_device(),
    )

    return bge_embedding

def load_nodes_to_milvus(nodes, dim =1024):
    # Embedding model
    bge_embedding = embedding_model(config.get_path('models', 'embedding'))
    # set the embedding model globally
    Settings.embed_model = bge_embedding

    # Create or get the vector store
    if os.path.exists(config.get('milvus')['uri']):
        # if the vector store already exists, load it
        print("Loading existing Milvus collection")
        vector_store = MilvusVectorStore(
            uri= config.get('milvus')['uri'],
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            storage_context=storage_context,
        )
        
    else:
        print("Creating new Milvus collection")
        vector_store = MilvusVectorStore(
            uri=config.get('milvus')['uri'],
            dim=dim,
            overwrite=True
        )
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        index = VectorStoreIndex(
            nodes=nodes,
            embed_model=Settings.embed_model,
            storage_context=storage_context,
        )
        # Persist the index and storage context

        index.storage_context.persist(config.get('milvus')['index_storage'])
        
        print(f"Index saved to {config.get('milvus')['index_storage']}")

    return index


