# Pipeline of the project

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import requests

base_url = "http://localhost:8888/api"

# CLS_NER Agent for Task Classification and Named Entity Recognition
def cls_ner_agent(query: str) -> dict:
    response = requests.post(f"{base_url}/ner", json={"query": query}).json().get("response")

    # parse the response, each line is a item
    lines = response.get("text").strip().split('\n')
    response_text = {}
    for line in lines:
        key, value = line.split(': ', 1)
        response_text[key.strip()] = value.strip()
    response['text'] = response_text

    return response

# RAG Agent for Question Answering
def rag_agent(query: str) -> dict:
    response = requests.post(f"{base_url}/rag", json={"query": query}).json().get("response")

    return response.get("response")

# SQL Agent for SQL Query Generation
def sql_agent(query: str):
    response = requests.post(f"{base_url}/sql", json={"query": query}).json().get("response")

    return response.get("response")

# Pipeline
def pipeline(query: str):
    cls_ner_output = cls_ner_agent(query)

    question_type = cls_ner_output.get("text").get("QuestionType")
    if question_type == '文本理解':
        return rag_agent(query)
    elif question_type == 'SQL查询':
        return sql_agent(query)
    else:
        return cls_ner_output
    
if __name__ == "__main__":
    query = "中国铁路通信信号有限公司发行前每股净资产为多少？"
    print(pipeline(query))

    query2 = "港股票日行情中哪一个股票的最高价最高？"
    print(pipeline(query2))
