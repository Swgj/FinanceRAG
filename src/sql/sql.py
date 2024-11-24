from llama_index.core import (
    PromptTemplate,
    Settings,
    SQLDatabase,
)
from llama_index.core.query_engine import NLSQLTableQueryEngine
from sqlalchemy import create_engine, MetaData
from llama_index.llms.ollama import Ollama
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from src.config import config
from src.utils.torch_utils import get_device
from src.prompt.text_to_sql_template import get_prompt


# create engine
db_path = config.get_path('dataset', 'db')
try:
    engine = create_engine(f'sqlite:///{db_path}')
except:
    raise Exception('Engine is not created, check the database path')

metadata = MetaData()
metadata.reflect(engine)

def get_query_engine():
    if config.get("llm") == "huggingface":
        Settings.llm = HuggingFaceLLM(
            model_name=config.get_path('models', 'sql'),
            tokenizer_name=config.get_path('models', 'sql'),
            )
    elif config.get("llm") == "ollama":
        Settings.llm = Ollama(model=config.get('models')['sql']) # do not change get to get_path, here's getting name
    else:
        raise Exception("Invalid LLM")
    
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=config.get_path('models', 'embedding'),
        device= get_device()
    )
    global engine, metadata
    sql_db = SQLDatabase(engine=engine, metadata=metadata)
    
    # create query engine
    query_engine = NLSQLTableQueryEngine(
        sql_database=sql_db,
        tables=list(metadata.tables.keys()),
        llm=Settings.llm,
        sql_only=True,
        synthesize_response=False,
        text_to_sql_prompt=get_prompt(),
    )
    return query_engine
