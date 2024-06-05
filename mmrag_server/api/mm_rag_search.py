from dataclasses import dataclass
from typing import List, Optional, Union

from config import Config
from core.logger import Log
from fastapi import APIRouter, Cookie, Path, Query, Response
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.base.llms.types import CompletionResponse
from llama_index.core.schema import NodeWithScore, QueryBundle
from models.models import ApiResponse, NoteData
from services.fetch_datas import deduplicated_nodes, kvdatas
from services.llm.ollama_embedding import (
    set_remote_embedding_model,
    set_remote_image_embedding_model,
)
from services.retriever.mm_retriver import (
    build_mm_rag_pipeline,
    response_post_processing,
)
from utils.response import resp_error, resp_success

router = APIRouter()


@dataclass
class RetrieverMeta:
    mm_retriever: BaseRetriever
    mm_query_engine: BaseQueryEngine
    template_nodes: Union[NodeWithScore, None]


global rem


@router.get("/embedding-mm")
async def embedding_mm(embed_mode: str = Query("auto", alias="embed_mode")):
    """
    API endpoint to set up the embedding model for multimodal retrieval.

    Args:
        embed_mode (str): The embedding mode to use. Defaults to "auto".

    Returns:
        ApiResponse: The API response indicating the success of the operation.
    """
    try:
        set_remote_embedding_model()
        set_remote_image_embedding_model()

        global rem
        similarity_top_k = 5
        image_similarity_top_k = 5
        retriever, query_engine = build_mm_rag_pipeline(
            embed_mode, similarity_top_k, image_similarity_top_k
        )
        Log.info(" Init embedding_mm")
        rem = RetrieverMeta(
            mm_retriever=retriever, mm_query_engine=query_engine, template_nodes=[]
        )

        return resp_success("success build mm rag pipeline", data="")
    except Exception as e:
        return resp_error(f"Failed to set up embedding model {str(e)}")


@router.get("/mm-rag-search")
async def search_notes(
    query: str = Query(None, alias="query"),
    search_topk: int = Query(15, alias="topk"),
    visable_topk: int = Query(6, alias="topk"),
):
    """
    API endpoint to search for the most similar notes based on a query.

    Args:
        query (str): The search query string used to retrieve relevant notes.
        search_topk (int): The number of most similar results to return. Defaults to 15.
        visable_topk (int): The number of visible results to return. Defaults to 6.

    Returns:
        ApiResponse: The API response containing the search results.
    """
    try:
        rem.mm_retriever.similarity_top_k = int(search_topk)
        retrieval_results: List[NodeWithScore] = rem.mm_retriever.retrieve(query)

        deduplicated_results = deduplicated_nodes(retrieval_results)

        deduplicated_results = deduplicated_results[
            0 : min(len(deduplicated_results), int(visable_topk))
        ]
        rem.template_nodes = deduplicated_results

        query_nodes: List[NoteData] = []
        for res_node in deduplicated_results:
            meta = res_node.metadata
            node_data = kvdatas.get(meta["note_id"], None)
            if node_data is not None:
                query_nodes.append(node_data)

        return resp_success("search success", {"search_nodes": query_nodes})
    except Exception as e:
        return resp_error(f"Failed to search notes {str(e)}")


@router.get("/mm-rag-query")
async def query_notes(query: str = Query(None, alias="query")):
    """
    API endpoint to perform question-answering using the LLAMA model.

    Args:
        query (str): The search query string used to retrieve relevant notes.

    Returns:
        ApiResponse: The API response containing the query response.
    """
    try:
        if len(rem.template_nodes) != 0:
            retrieval_nodes: List[NodeWithScore] = rem.template_nodes

            query_bundle = QueryBundle(query)
            response: CompletionResponse = rem.mm_query_engine.synthesize(
                query_bundle,
                nodes=retrieval_nodes,
            )
            rem.template_nodes = []

        else:
            response = rem.mm_query_engine.query(query)

        response_content = response_post_processing(response)

        return resp_success("query success", {"query_response": response_content})
    except Exception as e:
        return resp_error(f"Failed to query notes {str(e)}")
