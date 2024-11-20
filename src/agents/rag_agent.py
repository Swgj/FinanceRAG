from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.rag.data_to_milvus import load_nodes_to_milvus
from src.rag.document_parse import docs_parse
from src.rag.rag import get_query_engine, query
from src.config import config
from src.utils.torch_utils import torch_gc
import datetime


router = APIRouter()
rag_agent = None

class RAGRequest(BaseModel):
    query: str

class RAGAgent:
    def __init__(self):
        self.rag_agent_engine = get_query_engine()

    def get_response(self, query_text):
        return self.rag_agent_engine.query(query_text)
    
@router.post("/rag")
async def handel_rag_request(request: RAGRequest):
    global rag_agent
    if rag_agent is None:
        rag_agent = RAGAgent()
    
    response = rag_agent.get_response(request.query)
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