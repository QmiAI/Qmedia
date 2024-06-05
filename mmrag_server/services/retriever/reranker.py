from llama_index.core.postprocessor import LLMRerank, SentenceTransformerRerank

# from llama_index.postprocessor.cohere_rerank import CohereRerank


def build_reranker() -> SentenceTransformerRerank:
    # reranker = LLMRerank(llm=Settings.llm)

    # rerank 用到的模型:
    # https://docs.llamaindex.ai/en/stable/examples/node_postprocessor/SentenceTransformerRerank/

    reranker = SentenceTransformerRerank(
        model="cross-encoder/ms-marco-MiniLM-L-2-v2", top_n=10
    )

    return reranker
