from llama_index.llms.ollama import Ollama
from llama_index.core import Settings, get_response_synthesizer, PromptTemplate
from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.response_synthesizers import BaseSynthesizer
# from llama_index.embeddings.huggingface import HuggingFaceEmbedding
# from typing import Optional
from src.config import config
from src.utils.torch_utils import get_device
from src.prompt.classify_task_template_fewshot import get_prompt


class NERQueryEngine(CustomQueryEngine):

    # retriever: BaseRetriever
    # response_synthesizer: BaseSynthesizer
    llm: Ollama
    qa_prompt: PromptTemplate

    def custom_query(self, query_str: str):
        # nodes = self.retriever.retrieve(query_str)

        # context_str = "\n\n".join([n.node.get_content() for n in nodes])
        response = self.llm.complete(
            self.qa_prompt.format(query_str=query_str)
        )
        # response_obj = self.response_synthesizer.synthesize(response)
        return response
    
def get_query_engine():
    Settings.llm = Ollama(model=config.get('models')['ner'])
    # retriever = BaseRetriever()  # 根据实际情况初始化
    # response_synthesizer = BaseSynthesizer()  # 根据实际情况初始化
 
    global engine

    # create query engine
    query_engine = NERQueryEngine(
        # retriever=retriever,
        # response_synthesizer=response_synthesizer,
        llm=Settings.llm,
        qa_prompt=get_prompt()
    )

    return query_engine