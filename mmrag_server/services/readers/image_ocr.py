import os
from dataclasses import Field
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Dict, Generator, List, Optional, Type

import fsspec
import numpy as np
import requests
from llama_index.core import Document
from llama_index.core.multi_modal_llms.generic_utils import (
    encode_image,
    image_documents_to_base64,
)
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import DEFAULT_METADATA_TMPL, DEFAULT_TEXT_NODE_TMPL
from pydantic import BaseModel


class OCRResponse(BaseModel):
    index: int
    boxes: List
    text: str
    score: float
    font_size: int
    area: int
    image_width: int
    image_height: int
    text_proportion: float


class ImageOcrReader(BaseReader):
    def __init__(self, model_name, base_url, meta_reader_type=None):
        """Initialize the ImageOcrReader.

        Args:
            model_name (str): The name of the OCR model to be used.
            base_url (str): The base URL of the OCR API.
            meta_reader_type (str, optional): The type of the meta reader. Defaults to None.

        """
        self.model_name = model_name
        self.base_url = base_url
        self.meta_reader_type = meta_reader_type or self.get_reader_type()

    def get_reader_type(self):
        """Return the class name of the instance.

        Returns:
            dict: A dictionary containing the reader type.

        """
        return {"reader_type": self.__class__.__name__}

    def _get_text_from_model(self, img_str: str) -> List[OCRResponse]:

        # Check if img_str is a valid file path
        if not os.path.isfile(img_str):
            raise ValueError(f"Invalid file path: {img_str}")

        request_body = {
            "model": self.model_name,
            "image": encode_image(img_str),
        }

        response = requests.post(
            url=f"{self.base_url}/api/image-ocr",
            headers={"Content-Type": "application/json"},
            json=request_body,
        )
        response.encoding = "utf-8"
        if response.status_code != 200:
            optional_detail = response.json().get("error")
            raise ValueError(
                f"ImageOcrReader call failed with status code {response.status_code}."
                f" Details: {optional_detail}"
            )

        try:
            resp_list = response.json()
            resp_list = [OCRResponse.model_validate(r) for r in resp_list]
            return resp_list
        except requests.exceptions.JSONDecodeError as e:
            raise ValueError(
                f"Error raised for ImageOcrReader Call: {e}.\nResponse: {response.text}"
            )

    def _parse_ocrresponse_to_text(
        self, resp: List[OCRResponse], num_categories: int = 3
    ):
        """Parse OCRResponse objects to text.

        Args:
            resp (List[OCRResponse]): A list of OCRResponse objects.
            num_categories (int, optional): The number of categories to divide the font sizes into. Defaults to 3.

        Returns:
            str: The final parsed text.

        """
        # get font_size
        font_sizes = np.array([item.font_size for item in resp])

        # Calculating Quantiles
        quantiles = np.percentile(font_sizes, np.linspace(0, 100, num_categories + 1))

        # Divides font sizes into num_categories classes by quantile
        grouped_by_category = {i: [] for i in range(num_categories)}
        for item in resp:
            for i in range(num_categories):
                if quantiles[i] <= item.font_size <= quantiles[i + 1]:
                    grouped_by_category[i].append(item.text)
                    break

        combined_texts = []
        for category in sorted(grouped_by_category.keys()):
            combined_text = " ".join(grouped_by_category[category])
            combined_texts.append(combined_text)

        final_text = ". ".join(combined_texts)

        return final_text

    def load_data(self, file: str, **load_kwargs) -> List[Document]:
        """Load data from a file.

        Args:
            file (str): The path to the file.
            **load_kwargs: Additional keyword arguments for loading the data.

        Returns:
            List[Document]: A list of Document objects.

        """
        if not os.path.isfile(file):
            print(f"File {file} does not exist.")
            return []

        try:
            resp: List[OCRResponse] = self._get_text_from_model(file)
            # Parse image into text
            text_str: str = self._parse_ocrresponse_to_text(resp)

            load_kwargs.setdefault("metadata", {}).update(self.meta_reader_type)

            return [Document(text=text_str, **load_kwargs)]
        except Exception as e:
            print(f"Error raised for {str(e)}")
            return []
