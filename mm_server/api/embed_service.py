from typing import Any, Dict, List, Optional

from config import Config
from fastapi import APIRouter, FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from rich import print
from services.clip_service import clip_init_model
from services.llm_service import hf_init_model

router = APIRouter()


class EmbeddingRequest(BaseModel):
    prompt: str
    model: str
    options: Optional[Dict[str, Any]] = {}


class EmbeddingResponse(BaseModel):
    embedding: List[float]


class ImageEmbeddingRequest(BaseModel):
    image: str
    model: str
    options: Optional[Dict[str, Any]] = {}


@router.post(
    "/api/embeddings", response_class=JSONResponse, response_model=EmbeddingResponse
)
async def generate_embeddings(request: EmbeddingRequest):
    """
    Generate text embeddings.

    Parameters:
    - request: EmbeddingRequest object containing the prompt, model, and options.

    Returns:
    - JSONResponse containing the generated embedding.
    """
    try:
        print(request)
        prompt = request.prompt

        embedding: List[float] = hf_init_model().get_text_embedding(prompt)
        content = EmbeddingResponse(embedding=embedding)
        return JSONResponse(content=jsonable_encoder(content))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/api/clip-text-embeddings",
    response_class=JSONResponse,
    response_model=EmbeddingResponse,
)
async def generate_embeddings(request: EmbeddingRequest):
    """
    Generate text embeddings using the CLIP model.

    Parameters:
    - request: EmbeddingRequest object containing the prompt, model, and options.

    Returns:
    - JSONResponse containing the generated embedding.
    """
    try:
        prompt = request.prompt

        embedding: List[float] = clip_init_model().get_text_embedding(prompt)
        content = EmbeddingResponse(embedding=embedding)
        return JSONResponse(content=jsonable_encoder(content))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/api/clip-image-embeddings",
    response_class=JSONResponse,
    response_model=EmbeddingResponse,
)
async def generate_embeddings(request: ImageEmbeddingRequest):
    """
    Generate image embeddings using the CLIP model.

    Parameters:
    - request: ImageEmbeddingRequest object containing the image, model, and options.

    Returns:
    - JSONResponse containing the generated embedding.
    """
    try:
        model = request.model
        image = request.image

        embedding: List[float] = clip_init_model().get_image_embedding(image)
        content = EmbeddingResponse(embedding=embedding)
        return JSONResponse(content=jsonable_encoder(content))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
