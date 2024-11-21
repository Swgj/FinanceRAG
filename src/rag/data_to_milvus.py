from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
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


# def create_milvus_collection(collection_name=config.get('milvus')['collection_name'], dim=1024):
#     # dim should be 1024 for bge-large-zh-v1.5

#     # Connect to Milvus
#     connections.connect(alias="default",
#                         host=config.get('milvus')['host'],
#                         port=config.get('milvus')['port'])
#     # Create collection if not exists
#     if not Collection.exists(collection_name):
#         # Create collection schema
#         fields = [
#             FieldSchema(name="doc_id", dtype=DataType.VARCHAR, max_length=200, is_primary=True, auto_id=False),
#             FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=dim),
#             FieldSchema(name="filename", dtype=DataType.VARCHAR, max_length=200),
#             FieldSchema(name="header1", dtype=DataType.VARCHAR, max_length=200),
#             FieldSchema(name="")
#         ]
#         schema = CollectionSchema(fields, description="Document embeddings with chunking")
#         # Create collection
#         collection = Collection(name=collection_name, schema=schema)
#         print(f"Collection {collection_name} created")
#     else:
#         collection = Collection(name=collection_name)
#         print(f"Collection {collection_name} already exists, load successfully")
    
#     return collection

# def insert_embeddings_to_milvus(collection, doc_ids, embeddings):
#     insert_data = [
#         doc_ids,
#         embeddings.cpu().numpy().tolist() # Convert tensor to list
#     ]
#     collection.insert(insert_data)
#     # 创建索引
#     index_params = {"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 128}}
#     collection.create_index(field_name="embedding", index_params=index_params)
#     # 加载数据
#     collection.load()
#     print(f"Inserted {len(doc_ids)} embeddings to Milvus collection {collection.name}")