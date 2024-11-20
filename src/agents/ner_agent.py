from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.cls_ner.cls_ner import get_query_engine
from src.config import config
from src.utils.torch_utils import torch_gc
import datetime


router = APIRouter()
ner_agent = None

class NERRequest(BaseModel):
    query: str

class NERAgent:
    def __init__(self):
        self.ner_agent_engine = get_query_engine()

    def get_response(self, query_text):
        return self.ner_agent_engine.query(query_text)
    
@router.post("/ner")
async def handel_ner_request(request: NERRequest):
    global ner_agent
    if ner_agent is None:
        ner_agent = NERAgent()
    
    response = ner_agent.get_response(request.query)
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