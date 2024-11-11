from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.config import config
from src.utils.torch_utils import torch_gc
import datetime


class SQLRequest(BaseModel):
    prompt: str # The prompt to generate SQL query

class SQLAgent:
    def __init__(self, model_name: str, lora_model_name: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remode_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", trust_remode_code=True)
        self.model = PeftModel.from_pretrained(self.model, lora_model_name)
        self.model.merge_and_unload()
        self.model = self.model.eval()

    def generate_sql_query(self, request: SQLRequest):
        try:
            inputs = self.tokenizer(request.prompt, return_tensors="pt").to(self.model.device)
            outputs = self.model.generate(inputs.input_ids, max_new_tokens=512, do_sample=True)
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

            return {"response": response}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

router = APIRouter()
sql_agent = None

@router.post("/sql")
async def generate_sql_query(request: SQLRequest):
    global sql_agent
    if sql_agent is None:
        try:
            sql_agent = SQLAgent(config.get_path('models','sql'), config.get_path('lora','sql'))
        except Exception as e:
            raise HTTPException(status_code=500, detail="SQL Agent not initialized")
    
    response = sql_agent.generate_sql_query(request)
    answer = {
        "response": response["response"],
        "status": 200,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    log =f"[{answer['time']}] prompt: {request.prompt}, response: {response['response']}"
    print(log)
    torch_gc()

    return answer