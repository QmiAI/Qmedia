import re
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

from fsspec import AbstractFileSystem
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document, ImageDocument
from services.readers.base import _DefaultFileMetadataFunc, get_default_fs


def get_fs_info() -> _DefaultFileMetadataFunc:
    fs = get_default_fs()
    file_metadata = _DefaultFileMetadataFunc(fs)
    return file_metadata


class ImageReader(BaseReader):
    """Image parser.

    Extract text from images using DONUT or pytesseract.

    """

    get_file_metadata = get_fs_info()

    def __init__(self, meta_reader_type=None):
        self.meta_reader_type = meta_reader_type or self.get_reader_type()

    def get_reader_type(self):
        """Return the class name of the instance."""
        return {"reader_type": self.__class__.__name__}

    def load_data(self, file: str, **load_kwargs: Any) -> List[Document]:
        """Load data from an image file.

        Args:
            file (str): The path to the image file.
            **load_kwargs: Additional keyword arguments for loading the data.

        Returns:
            List[Document]: A list of ImageDocument objects containing the extracted text and image information.

        """
        file_extra_info = self.get_file_metadata(file)

        new_metadata = file_extra_info
        new_excluded_llm_keys = []  # list(file_extra_info.keys())
        new_excluded_embed_keys = []  # list(file_extra_info.keys())

        # 使用setdefault
        load_kwargs.setdefault("metadata", {}).update(new_metadata)
        load_kwargs.setdefault("metadata", {}).update(self.meta_reader_type)
        load_kwargs.setdefault("excluded_llm_metadata_keys", []).extend(
            new_excluded_llm_keys
        )
        load_kwargs.setdefault("excluded_embed_metadata_keys", []).extend(
            new_excluded_embed_keys
        )

        image_str: Optional[str] = ""
        text_str: str = ""
        return [ImageDocument(text=text_str, image_path=file, **load_kwargs)]
