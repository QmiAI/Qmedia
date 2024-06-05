from io import BytesIO
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from rich import print
from services.video_service import video_init_model

router = APIRouter()


class SentenceSegment(BaseModel):
    id: int
    seek: int
    start: float
    end: float
    text: str


class AudioResponse(BaseModel):
    language: str
    language_probability: float
    duration: float
    duration_after_vad: float
    segments: List[SentenceSegment]


@router.post(
    "/api/audio_transcription",
    response_class=JSONResponse,
    response_model=AudioResponse,
)
async def audio_transcription(file: UploadFile = File(...), model: str = Form()):
    """
    Transcribes the audio from the uploaded file.

    Parameters:
    - file: UploadFile object representing the audio file to be transcribed.
    - model: Optional string specifying the model to be used for transcription.

    Returns:
    - JSONResponse: Response object containing the transcription result.

    """
    try:
        byteio = BytesIO(await file.read())
        resp = video_init_model().get_audio_transcription(byteio)
        return JSONResponse(content=jsonable_encoder(resp))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
