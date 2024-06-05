from config import Config
from llama_index.core import Document, Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.embeddings import resolve_embed_model
from llama_index.core.multi_modal_llms import MultiModalLLM, MultiModalLLMMetadata
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama


def set_embedding_model():
    try:
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    except ImportError:
        raise ImportError(
            "Could not import llama_index.embeddings.huggingface library."
            "Please install requests with `pip install llama-index-embeddings-huggingface`"
        )

    Settings.embed_model = HuggingFaceEmbedding(model_name=Config.embedding_model_name)
    Settings.embed_model.callback_manager = Settings.callback_manager

    # ollama
    Settings.llm = Ollama(
        model=Config.model_name, base_url=Config.ollama_url, request_timeout=100000
    )


def set_remote_embedding_model():
    from services.llm.remote_embedding import RemoteHuggingFaceEmbedding

    Settings.embed_model = RemoteHuggingFaceEmbedding(
        model_name=Config.embedding_model_name, base_url=Config.mm_server_url
    )

    Settings.embed_model.callback_manager = Settings.callback_manager

    # ollama
    Settings.llm = Ollama(
        model=Config.model_name, base_url=Config.ollama_url, request_timeout=100000
    )


def set_remote_image_embedding_model():
    from services.llm.remote_embedding import RemoteClipEmbedding

    # from llama_index.multi_modal_llms.ollama import OllamaMultiModal
    # Settings.mm_llm_model = OllamaMultiModal(base_url=Config.ollama_url,
    # model=Config.mm_model_name)
    image_embed_model = RemoteClipEmbedding(
        base_url=Config.mm_server_url, model_name=Config.clip_model_name
    )

    Settings.image_embed_model = image_embed_model
