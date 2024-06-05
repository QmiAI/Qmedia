import json
from typing import List

from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import BaseNode, IndexNode
from llama_index.readers.json import JSONReader
from models.models import NoteData


def build_documents(json_file_path: str) -> List[Document]:
    with open(json_file_path, "r", encoding="utf-8") as f:
        datas: List[NoteData] = json.load(f)
    print(json_file_path)
    extra_info = []
    for data in datas:
        _ext = data["info_data"]
        extra_info.append({"id": _ext["id"], "note_id": _ext["note_id"]})
    reader = JSONReader()
    documents = reader.load_data(input_file=json_file_path, extra_info=extra_info)
    # index = VectorStoreIndex.from_documents(document)
    # query_engine = index.as_query_engine()
    return documents


def build_nodes(documents: List[Document]):
    # 尝试不同的分块策略
    # initialize modules
    # chunk_sizes = [128, 256, 512, 1024]
    chunk_sizes = [128, 256, 512]
    nodes_list = []
    vector_indices = []
    for chunk_size in chunk_sizes:
        print(f"Chunk Size: {chunk_size}")
        splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=10)
        nodes: List[BaseNode] = splitter.get_nodes_from_documents(documents)

        # add chunk size to nodes to track later
        for node in nodes:
            node.metadata["chunk_size"] = chunk_size
            node.excluded_embed_metadata_keys = ["chunk_size"]
            node.excluded_llm_metadata_keys = ["chunk_size"]

        nodes_list.append(nodes)

        # build vector index
        vector_index = VectorStoreIndex(nodes)
        vector_indices.append(vector_index)

    # Define Ensemble Retriever
    # 不同块节点进行检索, 然后重排
    # try ensemble retrieval

    # retriever_tools = []
    retriever_dict = {}
    retriever_nodes = []
    for chunk_size, vector_index in zip(chunk_sizes, vector_indices):
        node_id = f"chunk_{chunk_size}"
        node = IndexNode(
            text=(f"(chunk size {chunk_size})"),
            index_id=node_id,
        )
        retriever_nodes.append(node)
        retriever_dict[node_id] = vector_index.as_retriever()

    return retriever_nodes, retriever_dict
