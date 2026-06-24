import os
from typing import List, Optional

from cachetools import TTLCache, cached
from config import Config
from rich import print

try:
    from twelvelabs import TwelveLabs
    from twelvelabs.types.video_context import VideoContext_Url
except ImportError as e:
    print(f"Error importing twelvelabs SDK: {str(e)}")

twelvelabs_cached = TTLCache(maxsize=1, ttl=Config.twelvelabs_keep_alive)

Embedding = List[float]


def _api_key() -> str:
    """Read the TwelveLabs API key from the environment (never hard-coded)."""
    key = os.environ.get("TWELVELABS_API_KEY")
    if not key:
        raise RuntimeError(
            "TWELVELABS_API_KEY is not set. Export it to enable the TwelveLabs "
            "backend, or get a free key at https://twelvelabs.io"
        )
    return key


class TwelveLabsRemote:
    """Optional TwelveLabs backend.

    Wraps the official `twelvelabs` SDK to expose:
    - Marengo multimodal text embeddings (512-dim), matching the shape returned
      by the CLIP/HuggingFace embedders used elsewhere in mm_server.
    - Pegasus video understanding for caption/analysis generation from a video URL.
    """

    def __init__(self):
        self._client = TwelveLabs(api_key=_api_key())

    def get_text_embedding(self, prompt: str) -> Embedding:
        """Embed text with Marengo and return a flat float vector."""
        resp = self._client.embed.create(
            model_name=Config.twelvelabs_embed_model, text=prompt
        )
        return resp.text_embedding.segments[0].float_

    def get_video_analysis(
        self, video_url: str, prompt: str, max_tokens: Optional[int] = None
    ) -> str:
        """Analyse a video with Pegasus and return the generated text.

        TwelveLabs fetches the video server-side from `video_url`, so the file
        must be a publicly reachable URL.
        """
        resp = self._client.analyze(
            model_name=Config.twelvelabs_analyze_model,
            video=VideoContext_Url(url=video_url),
            prompt=prompt,
            max_tokens=max_tokens or Config.twelvelabs_max_tokens,
        )
        return resp.data


@cached(twelvelabs_cached)
def twelvelabs_init_model() -> TwelveLabsRemote:
    print(f"@ Init TwelveLabsRemote model server")
    return TwelveLabsRemote()


def test(prompt: str = "a cat playing piano"):
    embedding: List[float] = twelvelabs_init_model().get_text_embedding(prompt)
    print(len(embedding))
    print(embedding)
