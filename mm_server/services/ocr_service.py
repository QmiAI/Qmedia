import base64
from pathlib import Path
from typing import List

import cv2
import numpy as np
from cachetools import TTLCache, cached, keys
from config import Config
from llama_index.core.schema import *
from PIL import Image
from rich import print
from services.ocr_server.ocr import OCQanythingRModel, OCRResponse

ocr_cached = TTLCache(maxsize=1, ttl=Config.ocr_keep_alive)


def decode_base64_image(base64_str: str) -> Image:
    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data))
    image_rgb = image.convert("RGB")
    return image_rgb


class OCRRemote(OCQanythingRModel):
    def get_image_ocr(self, img_file_path: ImageType) -> List[OCRResponse]:
        try:
            if not isinstance(img_file_path, str):
                raise ValueError("img_file_path must be a string")
            image_rgb = decode_base64_image(img_file_path)
            image_rgb = np.array(image_rgb)
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
            ocr_reps: List[OCRResponse] = self(image_bgr)
            return ocr_reps
        except Exception as e:
            print(f"Error processing image: {e}")
            return []


# ocr_model = OCRRemote(model_dir=Config.ocr_model_path, device='cpu')
# print("Load ocr_model")


@cached(ocr_cached)
def ocr_init_model():
    print(f"@ Init OCRRemote model server")
    model = OCRRemote(model_dir=Config.ocr_model_path, device="cpu")
    return model


def test(img_file_path: str):
    from llama_index.core.multi_modal_llms.generic_utils import encode_image

    image_base64 = encode_image(img_file_path)
    ocr_reps: List[OCRResponse] = ocr_init_model().get_image_ocr(image_base64)
    ocr_reps = ocr_reps[0 : min(3, len(ocr_reps))]
    print(len(ocr_reps))
    print(ocr_reps)
