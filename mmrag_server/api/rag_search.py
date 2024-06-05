import asyncio
from dataclasses import dataclass
from typing import List, Optional

from config import Config
from fastapi import APIRouter, Cookie, Path, Query, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from llama_index.core import Document, Settings, VectorStoreIndex
from llama_index.core.schema import BaseNode, IndexNode
from llama_index.core.vector_stores import VectorStoreQuery, VectorStoreQueryResult
from models.models import ApiResponse, NoteData
from pydantic import BaseModel, Field
from services.doc_process.model_data import build_documents, build_nodes
from services.retriever.simple_retriever import VectorStore3B
from utils.response import resp_error, resp_success

router = APIRouter()


@dataclass
class RetrieverMeta:
    pass


rem = RetrieverMeta()


@router.get("/embedding")
async def embedding_datas():
    # 1. 设置embedding models
    from services.llm.ollama_embedding import set_remote_embedding_model

    set_remote_embedding_model()

    # 2. 获得编码数据
    documents: List[Document] = build_documents(Config.json_file_path)

    nodes: List[BaseNode] = build_nodes(documents)

    vector_store = VectorStore3B()
    vector_store.add(nodes)
    rem.vector_store = vector_store

    return resp_success("sucess build documents", data="")


@router.get("/rag-search")
async def search_notes(
    query: str = Query(None, alias="query"), topk: int = Query(5, alias="topk")
):
    """
    简介:
        返回最相近的notes

    Args:
        query (str): 搜索查询语句。是一个字符串，用于检索相关的笔记。
        topk (int): 返回的最相似结果的数量。默认值为5，表示返回相似度最高的前5个结果。

    example:
        `http://localhost/rag-search/?query=SEO如何构建`
    """

    print(query)
    from services.fetch_datas import kvdatas

    query_embedding = Settings.embed_model.get_query_embedding(query)

    query_obj = VectorStoreQuery(
        query_embedding=query_embedding, similarity_top_k=int(topk)
    )

    query_result = rem.vector_store.query(query_obj)
    print(len(query_result.nodes))
    query_nodes: List[NoteData] = []
    for similarities, node in zip(query_result.similarities, query_result.nodes):
        if similarities < Config.similarities_thre:
            continue

        node_data = kvdatas.get(node.metadata["note_id"], None)
        if node_data is not None:
            query_nodes.append(node_data)

    for similarity, node in zip(query_result.similarities, query_result.nodes):
        # print(node)
        print(
            "\n----------------\n"
            f"[Node ID {node.node_id}] Similarity: {similarity}"
            # f"{node.get_content(metadata_mode='all')}"
            # f"{node.metadata}"
            "\n----------------\n"
        )

    return resp_success("search sucesss", {"search_nodes": query_nodes})


@router.get("/rag-query")
async def search_notes(query: str = Query(None, alias="query")):
    """
    简介:
        根据query 使用llm进行问答

    Args:
        query (str): 搜索查询语句。是一个字符串，用于检索相关的笔记。

    example:
        `http://localhost/rag-query/?query=SEO如何构建`
    """

    index = VectorStoreIndex.from_vector_store(rem.vector_store)
    query_engine = index.as_query_engine(llm=Settings.llm)
    response = query_engine.query(query)
    return resp_success("query sucesss", {"query_response": response.response})


class HistoryItem(BaseModel):
    query: str
    response: str


class ChatData(BaseModel):
    query: str = Field(..., example="", description="query 问题")
    history: Optional[List[HistoryItem]] = Field(
        default=None,
        example=[HistoryItem(query="query", response="response")],
        description="历史信息",
    )
    streaming: Optional[bool] = Field(
        default=False, example=False, description="流式模式"
    )


async def chat_stream_retrieval(query, history):
    from llama_index.core import VectorStoreIndex

    index = VectorStoreIndex.from_vector_store(rem.vector_store)
    query_engine = index.as_query_engine(
        llm=Settings.llm, streaming=True, similarity_top_k=3
    )
    streaming_response = query_engine.query(query)
    for token in streaming_response.response_gen:
        history = HistoryItem(query=query, response=token)
        msg: ApiResponse[HistoryItem] = resp_success("query sucesss", history)
        # json_data= json.dumps(msg.model_dump_json(), ensure_ascii=False).encode()
        json_data = msg.model_dump_json()
        yield json_data
    # response = query_engine.query(query_str)
    # print(str(response))


def chat_retrieval(query, history) -> HistoryItem:
    index = VectorStoreIndex.from_vector_store(rem.vector_store)
    query_engine = index.as_query_engine(llm=Settings.llm)
    response = query_engine.query(query)
    history = HistoryItem(query=query, response=response.response)
    return history


@router.post(
    "/rag-chat-query",
    response_class=JSONResponse,
    response_model=ApiResponse[HistoryItem],
)
async def handle_query(chat_data: ChatData):
    """
    与rag 内容进行对话

    参数:
        query: str = Field(..., example="")
        history: Optional[List[HistoryItem]] = Field(default=None, example=[HistoryItem(query="query", response="response")])
        streaming: Optional[bool] = Field(default=False, example=False)

    """
    print(chat_data.query)
    streaming = chat_data.streaming

    if streaming:
        return StreamingResponse(
            chat_stream_retrieval(chat_data.query, chat_data.history),
            media_type="application/json",
        )
    else:
        history: HistoryItem = chat_retrieval(chat_data.query, chat_data.history)
        return resp_success("query sucesss", history)
