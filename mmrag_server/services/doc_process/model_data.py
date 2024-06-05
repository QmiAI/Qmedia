from pathlib import Path
from typing import List

from llama_index.core import Document, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import BaseNode, IndexNode
from models.models import *


def build_documents(json_file_path: str) -> List[Document]:
    from services.fetch_datas import datas

    docs = []
    for data in datas:
        info_data: InfoData = data.info_data
        text = info_data.title + info_data.desc
        doc = Document(
            text=text,
            metadata={
                "id": info_data.id,
                "note_id": info_data.note_id,
                "title": info_data.title,
            },
        )
        docs.append(doc)
    return docs


def build_nodes(documents: List[Document]) -> List[BaseNode]:

    # NOTE: 不同的document 使用的方式不一样
    node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=10)
    nodes = node_parser.get_nodes_from_documents(documents)
    print("nodes count", len(nodes), len(documents))

    for node in nodes:
        node_embedding = Settings.embed_model.get_text_embedding(
            node.get_content(metadata_mode="all")
        )
        node.embedding = node_embedding

    return nodes
