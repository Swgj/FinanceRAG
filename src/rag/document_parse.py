from src.config import config
from llama_index.core import SimpleDirectoryReader
from llama_index.readers.file import FlatReader, MarkdownReader
from llama_index.core.node_parser import SimpleFileNodeParser, MarkdownNodeParser, MarkdownElementNodeParser
from pathlib import Path
from typing import List
# import os

def docs_parse(doc_dir: List[str]):
    docs = []
    for doc_path in doc_dir:
        doc = FlatReader().load_data(Path(doc_path))
        docs.extend(doc)

    parser = SimpleFileNodeParser()
    # parse the documents to nodes
    nodes = parser.get_nodes_from_documents(docs)
    return nodes

def docs_parse_markdown(doc_dir: List[str]):
    docs = SimpleDirectoryReader(
        input_files=doc_dir,
        file_extractor={".md": MarkdownReader()},
    ).load_data()

    node_parser = MarkdownNodeParser()
    nodes = node_parser.get_nodes_from_documents(docs)
    return nodes