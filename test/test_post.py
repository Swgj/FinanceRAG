# Testing post request works correctly
# First need to run the server
# python -m uvicorn src.app:app --reload --host localhost --port 8888

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests

base_url = "http://localhost:8888/api"

def test_ner_post():
    ner_response = requests.post(base_url + "/ner", json={"query": "中国铁路通信信号有限公司发行前每股净资产为多少？"})
    ner_response = ner_response.json()
    ner_response = ner_response.get("response")
    print(ner_response["text"])

def test_rag_post():
    rag_response = requests.post(base_url + "/rag", json={"query": "中国铁路通信信号有限公司发行前每股净资产为多少？"})
    print(rag_response.json())

def test_sql_post():
    sql_response = requests.post(base_url + "/sql", json={"query": "港股票日行情中哪一个股票的最高价最高？"})
    print(sql_response.json())

if __name__ == "__main__":
    print("Testing ner post...")
    test_ner_post()
    print("Testing rag post...")
    test_rag_post()
    print("Testing sql post...")
    test_sql_post()