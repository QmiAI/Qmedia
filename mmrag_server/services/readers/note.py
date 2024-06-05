import re
from pathlib import Path
from typing import Any, Dict, List, Optional, cast

from fsspec import AbstractFileSystem
from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document, ImageDocument
from models.models import ImageData, InfoData, NoteData, VideoData
from pydantic import Field

DEFAULT_TMPL = "{key}: {value}"
DEFAULT_SEPERATOR = "\n"


class NoteInfoReader(BaseReader):
    def __init__(
        self,
        content_template: str = DEFAULT_TMPL,
        content_seperator: str = DEFAULT_SEPERATOR,
        meta_reader_type=None,
    ):
        self.content_template = content_template
        self.content_seperator = content_seperator
        self.meta_reader_type = meta_reader_type or self.get_reader_type()

    def get_reader_type(self):
        """Return the class name of the instance."""
        return {"reader_type": self.__class__.__name__}

    def load_data(self, content: InfoData, **load_kwargs: Any) -> List[Document]:
        _info = {
            "title": content.title,
            "desc": content.desc,
            "tag_list": ",".join(content.tag_list),
        }
        text = self.content_seperator.join(
            [
                self.content_template.format(key=key, value=str(value))
                for key, value in _info.items()
            ]
        )

        load_kwargs.setdefault("metadata", {}).update(self.meta_reader_type)
        doc = Document(text=text, **load_kwargs)
        return [doc]
