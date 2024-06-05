import base64
from pathlib import Path
from typing import List

# import torch
from cachetools import TTLCache, cached, keys
from config import Config
from llama_index.core.schema import *
from llama_index.embeddings.clip import ClipEmbedding  # pants: no-infer-dep
from PIL import Image
from rich import print

clip_cached = TTLCache(maxsize=1, ttl=Config.clip_keep_alive)

Embedding = List[float]


def decode_base64_image(base64_str: str) -> Image:
    image_data = base64.b64decode(base64_str)
    return Image.open(BytesIO(image_data))


class ClipEmbeddingRemote(ClipEmbedding):
    """A class that represents a remote ClipEmbedding service."""

    def _get_image_embedding(self, img_file_path: ImageType) -> Embedding:
        """
        Get the embedding of an image file.

        Args:
            img_file_path (str): The path to the image file.

        Returns:
            Embedding: The embedding of the image.
        """
        self._model.eval()
        image = decode_base64_image(img_file_path)
        # with torch.no_grad():
        image = self._preprocess(image).unsqueeze(0).to(self._device)
        return self._model.encode_image(image).tolist()[0]


@cached(clip_cached)
def clip_init_model() -> ClipEmbeddingRemote:
    print(f"@ Init ClipEmbeddingRemote model server")
    model = ClipEmbeddingRemote(model_name=Config.clip_model_name)
    return model


# def update_ttl(new_ttl):
#     global clip_cached
#     clip_cached = TTLCache(maxsize=1, ttl=new_ttl)

# clip_image_embed_model = ClipEmbeddingRemote(model_name=Config.clip_model_name)


def test(img_file_path: str):
    from llama_index.core.multi_modal_llms.generic_utils import (
        encode_image,
        image_documents_to_base64,
    )

    image_base64 = encode_image(img_file_path)
    embedding: List[float] = clip_init_model().get_image_embedding(image_base64)
    print(len(embedding))
    print(embedding)
