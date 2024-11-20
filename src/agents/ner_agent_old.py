from transformers import AutoTokenizer, AutoModelForCausalLM
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from peft import PeftModel
from src.utils.torch_utils import torch_gc
from src.config import config
import datetime


class NERRequest(BaseModel):
    text: str # The text to analyze, query from user

class NERAgent:
    def __init__(self, model_name: str, lora_model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remode_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", trust_remode_code=True)
        self.model = PeftModel.from_pretrained(self.model, lora_model_name)
        self.model.merge_and_unload()
        self.model = self.model.eval()


    def recognize_intent_entities(self, request: NERRequest):
        try:
            response = self.ner_pipeline(request.text)
            return {"response": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    

router = APIRouter()
ner_agent = None

@router.post("/ner")
async def recognize_intent_entities(request: NERRequest):
    global ner_agent
    if ner_agent is None:
        try:
            ner_agent = NERAgent(config.get_path('models','ner'), config.get_path('lora','ner'))
        except Exception as e:
            raise HTTPException(status_code=500, detail="NER Agent not initialized")
    
    response = ner_agent.recognize_intent_entities(request)
    now = datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    answer = {
        "response": response['response'],
        "status": 200,
        "time": time
    }

    log =f"[{time}] prompt: {request.text}, response: {response['response']}"
    print(log)
    torch_gc()

    return answer

