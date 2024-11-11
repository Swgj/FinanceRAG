from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from llama_index import GPTSimpleVectorIndex, Document
from pymilvus import connections, Collection
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer
from src.config import config
from src.utils.torch_utils import torch_gc, get_device
import datetime
import os


class RAGRequest(BaseModel):
    query: str # The query comes from the user


class RAGAgent:
    def __init__(self):
        # Connect to Milvus
        connections.connect(alias="default", host="localhost", port="19530")
        self.collection = Collection("document_embeddings")
        
        # Initialize embedding model
        embedding_model_name = config.get_path('models', 'embedding')
        self.embedding_model = SentenceTransformer(embedding_model_name)

        # Load language model and tokenizer
        model_name = config.get_path('models', 'rag')
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", trust_remote_code=True)
        self.model.eval()

        # Use GPU if available
        self.device = get_device()
        self.model.to(self.device)

        # Initialize LlamaIndex
        self.index = GPTSimpleVectorIndex()

    def retrieve_documents(self, query: str, top_k=5):
        try:
            # Generate embeddings for the query
            query_embedding = self.embedding_model.encode(query, convert_to_tensor=True)

            # Serch Milvus
            search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
            results = self.collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=top_k,
                output_fields=["doc_id"]
            )

            # Get document IDs
            doc_ids = [hit.entity.get("doc_id") for hit in results[0]]
            
            # Retrieve original texts based on doc_ids
            documents = []
            txt_dir = config.get_path('dataset', 'pdf2txt')
            for doc_id in doc_ids:
                txt_path = os.path.join(txt_dir, doc_id)
                if os.path.exists(txt_path):
                    with open(txt_path, 'r', encoding='utf-8') as f:
                        text = f.read()
                        documents.append(Document(text))
                else:
                    print(f"Warning: Text file {txt_path} does not exist.")
            return documents
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving documents: {str(e)}")

    def generate_response(self, query: str, documents: list):
        try:
            # Use LlamaIndex to re-rank documents
            ranked_docs = self.index.rank_documents(query, documents)
            context = "\n\n".join([doc.text for doc in ranked_docs])
            prompt = f"Context:\n{context}\n\nQuestion:\n{query}\n\nAnswer:"
            
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                inputs.input_ids,
                max_new_tokens=512,
                do_sample=True,
                top_p=0.95,
                top_k=50,
                temperature=0.7
            )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

router = APIRouter()
rag_agent = None

@router.post("/rag")
async def handle_rag_request(request: RAGRequest):
    global rag_agent
    if not rag_agent:
        rag_agent = RAGAgent()
    documents = rag_agent.retrieve_documents(request.query)
    response = rag_agent.generate_response(request.query, documents)
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    answer = {
        "response": response,
        "status": 200,
        "time": time
    }
    log = f"[{time}] query: {request.query}, response: {response}"
    print(log)
    torch_gc()
    return answer