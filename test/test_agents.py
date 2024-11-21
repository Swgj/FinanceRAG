# Test all the agents in the agents module working correctly

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.cls_ner.cls_ner import get_query_engine as ner_query_engine
from src.rag.rag import get_query_engine as rag_query_engine
from src.sql.sql import get_query_engine as sql_query_engine


def test_ner_agent():
    ner_engine = ner_query_engine()
    query1 = "请帮我计算，在20210105，中信行业分类划分的一级行业为综合金融行业中，涨跌幅最大股票的股票代码是？涨跌幅是多少？百分数保留两位小数。股票涨跌幅定义为：（收盘价 - 前一日收盘价 / 前一日收盘价）* 100%。"
    response1 = ner_engine.query(query1)
    print(response1)

    query2 = "中国铁路通信信号有限公司发行前每股净资产为多少？"
    response2 = ner_engine.query(query2)
    print(response2)

def test_rag_agent():
    rag_engine = rag_query_engine()
    query = "中国铁路通信信号有限公司发行前每股净资产为多少？"
    response = rag_engine.query(query)
    print(response)

def test_sql_agent():
    sql_engine = sql_query_engine()
    query = "请帮我计算，在20210105，中信行业分类划分的一级行业为综合金融行业中，涨跌幅最大股票的股票代码是？涨跌幅是多少？百分数保留两位小数。股票涨跌幅定义为：（收盘价"
    response = sql_engine.query(query)
    print(response)

if __name__ == "__main__":
    print("Testing ner agent...")
    test_ner_agent()
    print("Testing rag agent...")
    test_rag_agent()
    print("Testing sql agent...")
    test_sql_agent()