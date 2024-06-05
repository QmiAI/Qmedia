import abc
from typing import Any, Coroutine, Dict, List, Optional

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.bridge.pydantic import Field
from llama_index.core.embeddings.multi_modal_base import MultiModalEmbedding
from llama_index.core.multi_modal_llms.generic_utils import (
    encode_image,
    image_documents_to_base64,
)
from llama_index.core.schema import ImageType

Embedding = List[float]


class RemoteHuggingFaceEmbedding(BaseEmbedding):
    """Class for RemoteHuggingFaceEmbedding embeddings."""

    base_url: str = Field(description="Base url the model is hosted by Ollama")
    model_name: str = Field(description="The Ollama model to use.")

    def __init__(
        self,
        model_name: str,
        base_url: str = "http://localhost:11434",
    ) -> None:
        super().__init__(model_name=model_name, base_url=base_url)

    @classmethod
    def class_name(cls) -> str:
        return "RemoteHuggingFaceEmbedding"

    def _get_query_embedding(self, query: str) -> List[float]:
        """Get query embedding."""
        return self.get_general_text_embedding(query)

    async def _aget_query_embedding(self, query: str) -> List[float]:
        """The asynchronous version of _get_query_embedding."""
        return self.get_general_text_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        """Get text embedding."""
        return self.get_general_text_embedding(text)

    async def _aget_text_embedding(self, text: str) -> List[float]:
        """Asynchronously get text embedding."""
        return self.get_general_text_embedding(text)

    def _get_text_embeddings(self, texts: List[str]) -> List[Embedding]:
        """Get text embeddings."""
        embeddings_list: List[Embedding] = []
        for text in texts:
            embeddings = self.get_general_text_embedding(text)
            embeddings_list.append(embeddings)

        return embeddings_list

    async def _aget_text_embeddings(self, texts: List[str]) -> List[Embedding]:
        """Asynchronously get text embeddings."""
        return self._get_text_embeddings(texts)

    def get_general_text_embedding(self, prompt: str) -> Embedding:
        """Get RemoteHuggingFaceEmbedding embedding."""
        try:
            import requests
        except ImportError:
            raise ImportError(
                "Could not import requests library."
                "Please install requests with `pip install requests`"
            )

        request_body = {
            "prompt": prompt,
            "model": self.model_name,
        }

        response = requests.post(
            url=f"{self.base_url}/api/embeddings",
            headers={"Content-Type": "application/json"},
            json=request_body,
        )
        response.encoding = "utf-8"
        if response.status_code != 200:
            optional_detail = response.json().get("error")
            raise ValueError(
                f"RemoteHuggingFace call failed with status code {response.status_code}."
                f" Details: {optional_detail}"
            )

        try:
            return response.json()["embedding"]
        except requests.exceptions.JSONDecodeError as e:
            raise ValueError(
                f"Error raised for RemoteHuggingFace Call: {e}.\nResponse: {response.text}"
            )


class RemoteClipEmbedding(MultiModalEmbedding, RemoteHuggingFaceEmbedding):
    """Base class for Multi Modal embeddings."""

    base_url: str = Field(description="Base url the model is hosted by Ollama")
    model_name: str = Field(description="The Ollama model to use.")

    def __init__(
        self,
        model_name: str,
        base_url: str = "http://localhost:11434",
    ) -> None:
        super().__init__(model_name=model_name, base_url=base_url)

    def class_name(cls) -> str:
        return "RemoteClipEmbedding"

    # TEXT EMBEDDINGS

    def get_general_text_embedding(self, prompt: str) -> Embedding:
        """Get RemoteClipEmbedding embedding."""
        try:
            import requests
        except ImportError:
            raise ImportError(
                "Could not import requests library."
                "Please install requests with `pip install requests`"
            )

        request_body = {
            "prompt": prompt,
            "model": self.model_name,
        }

        response = requests.post(
            url=f"{self.base_url}/api/clip-text-embeddings",
            headers={"Content-Type": "application/json"},
            json=request_body,
        )
        response.encoding = "utf-8"
        if response.status_code != 200:
            optional_detail = response.json().get("error")
            raise ValueError(
                f"RemoteHuggingFace call failed with status code {response.status_code}."
                f" Details: {optional_detail}"
            )

        try:
            return response.json()["embedding"]
        except requests.exceptions.JSONDecodeError as e:
            raise ValueError(
                f"Error raised for RemoteHuggingFace Call: {e}.\nResponse: {response.text}"
            )

    # IMAGE EMBEDDINGS

    async def _aget_image_embedding(self, img_file_path: ImageType) -> Embedding:
        return self._get_image_embedding(img_file_path)

    def _get_image_embedding(self, img_file_path: ImageType) -> Embedding:
        """Get RemoteClipEmbedding image embedding."""
        try:
            import requests
        except ImportError:
            raise ImportError(
                "Could not import requests library."
                "Please install requests with `pip install requests`"
            )

        request_body = {
            "model": self.model_name,
            "image": encode_image(img_file_path),
        }

        response = requests.post(
            url=f"{self.base_url}/api/clip-image-embeddings",
            headers={"Content-Type": "application/json"},
            json=request_body,
        )
        response.encoding = "utf-8"
        if response.status_code != 200:
            optional_detail = response.json().get("error")
            raise ValueError(
                f"RemoteHuggingFace call failed with status code {response.status_code}."
                f" Details: {optional_detail}"
            )

        try:
            return response.json()["embedding"]
        except requests.exceptions.JSONDecodeError as e:
            raise ValueError(
                f"Error raised for RemoteHuggingFace Call: {e}.\nResponse: {response.text}"
            )
