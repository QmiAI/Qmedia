import os
from pathlib import Path
from typing import Dict, List

from config import Config
from llama_index.core import (
    Document,
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.indices.base import BaseIndex
from llama_index.core.storage.docstore import SimpleDocumentStore
from models.models import ImageData, InfoData, NoteData, VideoData
from tqdm import tqdm
from utils.http_utils import merge_path


def load_rawdata_from_local() -> List[NoteData]:
    from services.fetch_datas import datas

    return datas


def persist_documents(note_docs):
    # docs = []
    # for _docs in note_docs.values():
    #     docs.extend(_docs)

    docstore = SimpleDocumentStore(namespace=Config.db_index_id)
    docstore.add_documents(note_docs)
    docstore.persist(Config.docs_persist_path)
    print(f" @ Storge docs to {Config.docs_persist_path}")


def load_documents_from_persist() -> List[Document]:
    # SimpleDocumentStore 加载 json doc文件
    docstore = SimpleDocumentStore.from_persist_path(
        Config.docs_persist_path, namespace=Config.db_index_id
    )
    return list(docstore.docs.values())


def persist_index(index: BaseIndex):
    index_id = Config.db_index_id
    db_path = Config.db_path

    index.set_index_id(index_id)
    index.storage_context.persist(str(db_path))


def load_index_from_persist():
    from services.llm import (
        set_remote_embedding_model,
        set_remote_image_embedding_model,
    )

    set_remote_embedding_model()
    set_remote_image_embedding_model()  # 使用LLM 模型

    index_id = Config.db_index_id
    db_path = Config.db_path

    mm_vector_store_args = {
        "image_embed_model": Settings.image_embed_model,
        "embed_model": Settings.embed_model,
        "show_progress": True,
    }
    storage_context = StorageContext.from_defaults(persist_dir=str(db_path))
    index = load_index_from_storage(storage_context, index_id, **mm_vector_store_args)
    return index
