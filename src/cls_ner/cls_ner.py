from llama_index.llms.ollama import Ollama
from llama_index.core import Settings, get_response_synthesizer, PromptTemplate
from llama_index.core.query_engine import CustomQueryEngine
from src.config import config
from src.utils.torch_utils import get_device
from src.prompt.classify_task_template_fewshot import get_prompt


class NERQueryEngine(CustomQueryEngine):

    llm: Ollama
    qa_prompt: PromptTemplate

    def custom_query(self, query_str: str):
        
        response = self.llm.complete(
            self.qa_prompt.format(query_str=query_str)
        )
        
        return response
    
def get_query_engine():
    Settings.llm = Ollama(model=config.get('models')['ner'])
 
    global engine

    # create query engine
    query_engine = NERQueryEngine(
        llm=Settings.llm,
        qa_prompt=get_prompt()
    )

    return query_engine