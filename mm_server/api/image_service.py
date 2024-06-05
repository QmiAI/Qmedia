from typing import Any, Dict, List, Optional

from fastapi import APIRouter, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from rich import print
from services.ocr_service import OCRResponse, ocr_init_model

router = APIRouter()


class ImageRequest(BaseModel):
    image: str
    model: str
    options: Optional[Dict[str, Any]] = {}


@router.post(
    "/api/image-ocr", response_class=JSONResponse, response_model=List[OCRResponse]
)
async def generate_embeddings(request: ImageRequest):
    """
    Generate OCR embeddings for the given image.

    Args:
        request (ImageRequest): The request object containing the model and image.

    Returns:
        JSONResponse: The response containing the OCR results.
    """
    try:
        model = request.model
        image = request.image

        resp: List[OCRResponse] = ocr_init_model().get_image_ocr(image)
        return JSONResponse(content=jsonable_encoder(resp))
    except Exception as e:
        return JSONResponse(content={"error": str(e)})
