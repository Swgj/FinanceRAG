from llama_index.core import (
    PromptTemplate,
    Settings,
    SQLDatabase,
)
from llama_index.core.query_engine import NLSQLTableQueryEngine
from sqlalchemy import create_engine, MetaData
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from src.config import config
from src.utils.torch_utils import get_device


# create engine
db_path = config.get_path('dataset', 'db')
try:
    engine = create_engine(f'sqlite:///{db_path}')
except:
    raise Exception('Engine is not created, check the database path')

metadata = MetaData()
metadata.reflect(engine)

def get_query_engine():
    Settings.llm = Ollama(model=config.get('models')['sql'])
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=config.get('models')['embedding'],
        device= get_device()
    )
    global engine, metadata
    sql_db = SQLDatabase(engine=engine, metadata=metadata)
    
    # create query engine
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_db,
        tables=list(metadata.tables.keys()),
        llm=Settings.llm
    )
    return query_engine
