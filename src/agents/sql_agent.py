from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.sql.sql import get_query_engine
from src.config import config
from src.utils.torch_utils import torch_gc
import datetime

router = APIRouter()
sql_agent = None

class SQLRequest(BaseModel):
    query: str

@router.post("/sql")
async def generate_sql_query(request: SQLRequest):
    global sql_agent
    if sql_agent is None:
        sql_agent = get_query_engine()
    
    try:
        response = sql_agent.query(request.query)
        answer = {
            "response": response,
            "status": 200,
            "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        log = f"Query: {request.query}, Response: {response}"
        print(log)
        torch_gc()
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))