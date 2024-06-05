# Define recursive retriever.
from typing import List, Optional

from config import Config
from llama_index.core import Settings, SummaryIndex
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.base.base_retriever import BaseRetriever
from llama_index.core.base.response.schema import RESPONSE_TYPE, Response
from llama_index.core.indices.base import BaseIndex
from llama_index.core.prompts.base import PromptTemplate
from llama_index.core.prompts.prompt_type import PromptType
from llama_index.core.query_engine import BaseQueryEngine, RetrieverQueryEngine
from llama_index.core.schema import NodeWithScore
from llama_index.multi_modal_llms.ollama import OllamaMultiModal
from services.nodes import build_index

text_qa_prompt_tmpl = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Given the context information and not prior knowledge, "
    "answer the query.\n"
    "Query: {query_str}\n"
    "Answer: "
)
text_qa_template = PromptTemplate(
    text_qa_prompt_tmpl, prompt_type=PromptType.QUESTION_ANSWER
)

image_qa_template = PromptTemplate(
    text_qa_prompt_tmpl, prompt_type=PromptType.QUESTION_ANSWER
)


def build_mm_rag_pipeline(
    mode="auto", similarity_top_k: int = 3, image_similarity_top_k: int = 4
):

    index: BaseIndex = build_index(mode)

    retriever = index.as_retriever(
        similarity_top_k=similarity_top_k, image_similarity_top_k=image_similarity_top_k
    )

    # query_engine = index.as_query_engine(llm=Settings.mm_llm_model, similarity_top_k=similarity_top_k,
    #  image_similarity_top_k=image_similarity_top_k)

    query_engine = RetrieverQueryEngine.from_args(
        retriever=retriever,
        llm=Settings.llm,
        similarity_top_k=similarity_top_k,
        text_qa_template=text_qa_template,
        image_qa_template=image_qa_template,
    )

    return retriever, query_engine


def response_post_processing(response: Response) -> str:
    # nodes: List[NodeWithScore] = response.source_nodes

    return response.response


# the derived retriever will just retrieve all nodes
def build_mm_retriever(
    index: BaseIndex,
    similarity_top_k: int = 3,
    image_similarity_top_k: int = 3,
) -> BaseRetriever:
    retriever = index.as_retriever(
        similarity_top_k=similarity_top_k, image_similarity_top_k=image_similarity_top_k
    )
    return retriever


def get_mm_retriev_response(
    retriever: BaseRetriever, query: str
) -> List[NodeWithScore]:
    # generate  retrieval results
    retrieval_results = retriever.retrieve(query)
    return retrieval_results


def build_mm_query(
    index: BaseIndex, similarity_top_k: int = 3, image_similarity_top_k: int = 3
) -> BaseQueryEngine:
    # 使用文本进行RAG
    mm_model = OllamaMultiModal(base_url=Config.ollama_url, model="llava-llama3")
    query_engine = index.as_query_engine(
        llm=mm_model,
        similarity_top_k=similarity_top_k,
        image_similarity_top_k=image_similarity_top_k,
    )
    return query_engine


def get_mm_query_response(query_engine: BaseQueryEngine, query: str) -> RESPONSE_TYPE:
    # generate  retrieval results
    response = query_engine.query(query)
    return response


def get_mm_chat_response(query_engine: BaseQueryEngine, query: str) -> RESPONSE_TYPE:
    # generate  retrieval results
    response = query_engine.query(query)
    return response
