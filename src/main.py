from fastapi import FastAPI
from src.agents.ner_agent import router as ner_router, NERAgent
from src.agents.sql_agent import router as sql_router, SQLAgent
from src.agents.rag_agent import router as rag_router, RAGAgent
from src.config import config
import uvicorn
import argparse
import os




def main():
    parser = argparse.ArgumentParser(description='API argparser')
    parser.add_argument('--port', type=str, default='8088', help='Port to run the API')
    parser.add_argument('--config', type=str, default='config.yaml', help='Path to the config file')
    args = parser.parse_args()

    app = FastAPI()

    # Include the routers
    app.include_router(ner_router)
    app.include_router(sql_router)
    app.include_router(rag_router)


    # Initialize the NER Agent
    global ner_agent
    ner_agent = NERAgent(config.get_path('models','ner'), config.get_path('lora','ner'))
    # Initialize the SQL Agent
    global sql_agent
    sql_agent = SQLAgent(config.get_path('models','sql'), config.get_path('lora','sql'))

    port = args.port
    uvicorn.run(app, host="localhost", port=int(port), workers=1)


if __name__ == "__main__":
    main()
    