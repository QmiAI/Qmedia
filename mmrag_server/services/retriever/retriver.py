from config import Config
from llama_index.core import SummaryIndex
from llama_index.core.base.response.schema import RESPONSE_TYPE
from llama_index.core.retrievers import RecursiveRetriever, RouterRetriever


# the derived retriever will just retrieve all nodes
def build_retriever(
    retriever_nodes, retriever_dict, query: str, reranker=None
) -> RESPONSE_TYPE:
    from llama_index.core.query_engine import RetrieverQueryEngine

    summary_index = SummaryIndex(retriever_nodes)

    retriever = RecursiveRetriever(
        root_id="root",
        retriever_dict={"root": summary_index.as_retriever(), **retriever_dict},
    )

    if reranker is None:
        query_engine = RetrieverQueryEngine(retriever)
    else:
        query_engine = RetrieverQueryEngine(retriever, node_postprocessors=[reranker])
    response = query_engine.query(query)
    return response
