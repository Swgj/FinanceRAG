# Description: This script is used to vectorlize the markdown files in the data folder
# You can use it before first time running RAG, so that the vectorlized data can be saved in Milvus
# Also you can choose not to run this script, and the RAG will vectorlize the markdown files automatically

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.rag.rag import get_query_engine


def main():

    print("Initializing query engine...")
    query_engine = get_query_engine()
    print("Query engine initialized")

    query = "中国铁路通信信号有限公司发行前每股净资产为多少？"
    print(f"Test query:{query}")
    res = query_engine.query(query)
    print(res)
    print("Test finished")


if __name__ == "__main__":
    main()
