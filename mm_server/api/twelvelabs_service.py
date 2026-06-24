from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from rich import print
from services.twelvelabs_service import twelvelabs_init_model

router = APIRouter()


class EmbeddingRequest(BaseModel):
    prompt: str
    model: str
    options: Optional[Dict[str, Any]] = {}


class EmbeddingResponse(BaseModel):
    embedding: List[float]


class VideoAnalyzeRequest(BaseModel):
    video_url: str
    prompt: str
    max_tokens: Optional[int] = None
    options: Optional[Dict[str, Any]] = {}


class VideoAnalyzeResponse(BaseModel):
    text: str


@router.post(
    "/api/twelvelabs-text-embeddings",
    response_class=JSONResponse,
    response_model=EmbeddingResponse,
)
async def generate_twelvelabs_text_embeddings(request: EmbeddingRequest):
    """
    Generate text embeddings using the TwelveLabs Marengo model.

    Opt-in backend: requires the TWELVELABS_API_KEY environment variable.

    Parameters:
    - request: EmbeddingRequest object containing the prompt, model, and options.

    Returns:
    - JSONResponse containing the generated 512-dim embedding.
    """
    try:
        prompt = request.prompt

        embedding: List[float] = twelvelabs_init_model().get_text_embedding(prompt)
        content = EmbeddingResponse(embedding=embedding)
        return JSONResponse(content=jsonable_encoder(content))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/api/twelvelabs-video-analyze",
    response_class=JSONResponse,
    response_model=VideoAnalyzeResponse,
)
async def generate_twelvelabs_video_analysis(request: VideoAnalyzeRequest):
    """
    Analyse a video using the TwelveLabs Pegasus model.

    TwelveLabs fetches the video server-side from `video_url`, so it must be a
    publicly reachable URL. Opt-in backend: requires the TWELVELABS_API_KEY
    environment variable.

    Parameters:
    - request: VideoAnalyzeRequest object with the video_url, prompt, and options.

    Returns:
    - JSONResponse containing the generated analysis text.
    """
    try:
        text: str = twelvelabs_init_model().get_video_analysis(
            request.video_url, request.prompt, request.max_tokens
        )
        content = VideoAnalyzeResponse(text=text)
        return JSONResponse(content=jsonable_encoder(content))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
