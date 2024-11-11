from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
from src.rag.embedding_generator import load_texts, generate_embeddings
from src.config import config
import os

def create_milvus_collection(collection_name, dim=512):
    connections.connect(alias="default", host="localhost", port="19530")

    if not Collection.exists(collection_name):
        fields = [
            FieldSchema(name="doc_id", dtype=DataType.VARCHAR, max_length=200, is_primary=True, auto_id=False),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=512)
        ]
        schema = CollectionSchema(fields, description="Document embeddings")
        collection = Collection(name=collection_name, schema=schema)
        print(f"Collection {collection_name} created")
    else:
        collection = Collection(name=collection_name)
        print(f"Collection {collection_name} already exists, load successfully")
    
    return collection

def insert_embeddings_to_milvus(collection, doc_ids, embeddings):
    insert_data = [
        doc_ids,
        embeddings.cpu().numpy().tolist() # Convert tensor to list
    ]
    collection.insert(insert_data)
    # 创建索引
    index_params = {"index_type": "IVF_FLAT", "metric_type": "COSINE", "params": {"nlist": 128}}
    collection.create_index(field_name="embedding", index_params=index_params)
    # 加载数据
    collection.load()
    print(f"Inserted {len(doc_ids)} embeddings to Milvus collection {collection.name}")