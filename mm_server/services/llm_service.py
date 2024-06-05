import os
from pathlib import Path
from typing import List

import numpy as np
from cachetools import TTLCache, cached, keys
from config import Config
from llama_index.core import Settings
from llama_index.core.schema import *
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from rich import print

# hugface_embed_model = HuggingFaceEmbedding(
#                 model_name=Config.hf_embedding_model_name
#             )
# hugface_embed_model.callback_manager = Settings.callback_manager
# print(f" Load {hugface_embed_model.class_name()}")

hf_cached = TTLCache(maxsize=1, ttl=Config.hf_keep_alive)


@cached(hf_cached)
def hf_init_model():
    print(f"@ Init HuggingFaceEmbedding model server")
    model = HuggingFaceEmbedding(model_name=Config.hf_embedding_model_name)
    model.callback_manager = Settings.callback_manager
    return model


def test(prompt: str = "test"):
    embedding: List[float] = hf_init_model().get_text_embedding(prompt)
    print(len(embedding))
    print(embedding)
