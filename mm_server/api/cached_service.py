from cachetools import TTLCache
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from rich import print
from services.clip_service import clip_cached
from services.llm_service import hf_cached
from services.ocr_service import ocr_cached
from services.video_service import video_cached

MODEL_CACHED = {
    "clip": clip_cached,
    "hf": hf_cached,
    "video": video_cached,
    "ocr": ocr_cached,
}

router = APIRouter()


class ModelConfig(BaseModel):
    model_name: str
    keep_alive: int  # 5min
    hold_forever: bool = False


@router.post("/api/set-keep-alive")
async def set_model_config(config: ModelConfig):
    """
    API endpoint to set the keep-alive configuration for a specific model or all models.

    Parameters:
    - config: ModelConfig object containing the model_name, keep_alive, and hold_forever parameters.

    Returns:
    - Dictionary with a "message" key indicating the success of the configuration update.
    """
    global MODEL_CACHED

    def set_model_cache(model_name, keep_alive):
        global MODEL_CACHED
        try:
            MODEL_CACHED[model_name].clear()
            MODEL_CACHED[model_name] = TTLCache(maxsize=1, ttl=keep_alive)
            print(f"model: {model_name}, ttl: {keep_alive}")
        except KeyError:
            return {"message": f"Model '{model_name}' does not exist"}

    if config.hold_forever:
        keep_alive = None
    else:
        keep_alive = config.keep_alive

    if config.model_name == "all":
        for k in MODEL_CACHED.keys():
            set_model_cache(k, keep_alive)
    else:
        set_model_cache(config.model_name, keep_alive)

    return JSONResponse(content="Configuration updated successfully")
