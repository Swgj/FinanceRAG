import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from fastapi import FastAPI
from src.agents.sql_agent import router as sql_router
from src.agents.rag_agent import router as rag_router
from src.agents.ner_agent import router as ner_router

app = FastAPI()

app.include_router(sql_router, prefix='/api')
app.include_router(rag_router, prefix='/api')
app.include_router(ner_router, prefix='/api')

@app.get("/")
def read_root():
    return {"message": "Hello World"}