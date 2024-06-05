import os
from pathlib import Path
from typing import Dict, List

from config import Config
from core.logger import Log
from llama_index.core import Document, Settings
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.core.indices.base import BaseIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.readers.base import BaseReader
from models.models import ImageData, InfoData, NoteData, VideoData
from services.readers import (
    AudioTranscriptionReader,
    ImageOcrReader,
    ImageReader,
    NoteInfoReader,
)
from services.storage import *
from tqdm import tqdm
from utils.http_utils import merge_path


def build_index(mode="auto"):
    """
    Build the index based on the specified mode.

    Parameters:
        mode (str): The mode for building the index. Default is "auto".

    Returns:
        dict: The built index.

    Raises:
        ValueError: If an invalid mode is provided.
    """
    if mode == "auto":
        if os.path.exists(Config.db_path) and os.path.exists(Config.docs_persist_path):
            mode = "nodes_from_persist"
        elif os.path.exists(Config.docs_persist_path):
            mode = "docs_from_persist"
        else:
            mode = "raw"

    # 从原始数据构建
    if mode == "raw":
        # build docs, nodes, index
        raw_notes: List[NoteData] = load_rawdata_from_local()
        index, note_docs = build_index_from_rawdata(raw_notes)
        # 存储node
        persist_index(index)
        # 存储note_docs
        persist_documents(note_docs)

    elif mode == "docs_from_persist":
        # build nodes, index
        note_docs = load_documents_from_persist()
        nodes = build_nodes(note_docs)
        index = build_store_index(nodes)

    elif mode == "nodes_from_persist":
        # build index
        index = load_index_from_persist()
    else:
        raise ValueError

    return index


def build_index_from_rawdata(raw_notes):
    """
    Builds an index from raw notes data.

    Args:
        raw_notes (list): A list of raw notes.

    Returns:
        tuple: A tuple containing the index and the note documents.
    """
    try:
        image_readers = [
            ImageReader(),
            ImageOcrReader(
                model_name=Config.ocr_model_name, base_url=Config.ocr_reader_base_url
            ),
            # ImageLayoutReader(),
            # ImageCaptionReader(),
        ]

        video_readers = []
        if Config.use_video_service:
            video_readers = [
                AudioTranscriptionReader(
                    model_name=Config.video_model_name,
                    base_url=Config.video_reader_base_url,
                    parse_summary=True,
                    audio_trans=True,
                )
            ]

        text_readers = [NoteInfoReader()]

        note_docs = build_documents(
            raw_notes, image_readers, video_readers, text_readers
        )

        nodes = build_nodes(note_docs)
        index = build_store_index(nodes)

        return (index, note_docs)
    except Exception as e:
        raise RuntimeError(f"Error building index from raw data: {str(e)}")


def build_store_index(nodes):
    try:
        index = MultiModalVectorStoreIndex(
            nodes,
            show_progress=True,
            image_embed_model=Settings.image_embed_model,
            embed_model=Settings.embed_model,
        )
        return index
    except Exception as e:
        raise RuntimeError(f"Error building store index: {str(e)}")


def build_nodes(note_docs):
    try:
        node_parser = SentenceSplitter.from_defaults()

        # _image_docs = []
        # _text_docs = []
        # for doc in note_docs:
        #     if isinstance(doc, ImageDocument):
        #         _image_docs.append(doc)
        #     else:
        #         _text_docs.append(doc)
        nodes = node_parser.get_nodes_from_documents(note_docs)
        return nodes
    except Exception as e:
        raise RuntimeError(f"Error build_nodes: {str(e)}")


def build_documents(
    notes: List[NoteData],
    image_readers: List[BaseReader],
    video_readers: List[BaseReader],
    text_readers: List[BaseReader],
) -> Dict[str, List[Document]]:

    documents: Dict[str, List[Document]] = {}

    print(" @ Start vectorizing data from assets")

    for note in tqdm(notes):
        try:
            note_docs: List[Document] = []
            image_data: ImageData = note.image_data
            video_data: VideoData = note.video_data
            info_data: InfoData = note.info_data
            note_id = info_data.note_id

            image_local_paths = [
                merge_path(Config.local_store_path, name)
                for name in image_data.image_ids
            ]
            video_local_paths = [
                merge_path(Config.local_store_path, name)
                for name in video_data.video_ids
            ]

            note_doc_kwargs = {
                "metadata": {
                    "note_id": note_id,
                },
                "excluded_llm_metadata_keys": ["note_id"],
                "excluded_embed_metadata_keys": ["note_id"],
            }

            # image read pipeline
            for path in image_local_paths:
                for _reader in image_readers:
                    _docs = _reader.load_data(path, **note_doc_kwargs)
                    note_docs.extend(_docs)

            # video read pipeline
            for path in video_local_paths:
                for _reader in video_readers:
                    _docs = _reader.load_data(path, **note_doc_kwargs)
                    note_docs.extend(_docs)

            # text read pipeline
            for _reader in text_readers:
                _docs = _reader.load_data(info_data, **note_doc_kwargs)
                note_docs.extend(_docs)

            documents[note_id] = note_docs
        except Exception as e:
            print(f"Error processing note: {note} \nerror info: {str(e)}")

    docs = []
    for _docs in documents.values():
        docs.extend(_docs)
    return docs
