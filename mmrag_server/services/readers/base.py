import mimetypes
import os
from datetime import datetime
from typing import Any, Callable, Dict, Generator, List, Optional, Type

import fsspec
from fsspec.implementations.local import LocalFileSystem


def _format_file_timestamp(timestamp: float) -> Optional[str]:
    """Format file timestamp to a %Y-%m-%d string.

    Args:
        timestamp (float): timestamp in float

    Returns:
        str: formatted timestamp
    """
    try:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    except Exception:
        return None


def default_file_metadata_func(
    file_path: str, fs: Optional[fsspec.AbstractFileSystem] = None
) -> Dict:
    """Get some handy metadata from filesystem.

    Args:
        file_path: str: file path in str
    """
    fs = fs or get_default_fs()
    stat_result = fs.stat(file_path)

    try:
        file_name = os.path.basename(str(stat_result["name"]))
    except Exception as e:
        file_name = os.path.basename(file_path)

    creation_date = _format_file_timestamp(stat_result.get("created"))
    last_modified_date = _format_file_timestamp(stat_result.get("mtime"))
    last_accessed_date = _format_file_timestamp(stat_result.get("atime"))
    default_meta = {
        "file_path": file_path,
        "file_name": file_name,
        "file_type": mimetypes.guess_type(file_path)[0],
        "file_size": stat_result.get("size"),
        "creation_date": creation_date,
        "last_modified_date": last_modified_date,
        "last_accessed_date": last_accessed_date,
    }

    # Return not null value
    return {
        meta_key: meta_value
        for meta_key, meta_value in default_meta.items()
        if meta_value is not None
    }


class _DefaultFileMetadataFunc:
    """
    Default file metadata function wrapper which stores the fs.
    Allows for pickling of the function.
    """

    def __init__(self, fs: Optional[fsspec.AbstractFileSystem] = None):
        self.fs = fs or get_default_fs()

    def __call__(self, file_path: str) -> Dict:
        return default_file_metadata_func(file_path, self.fs)


def get_default_fs() -> fsspec.AbstractFileSystem:
    return LocalFileSystem()


def is_default_fs(fs: fsspec.AbstractFileSystem) -> bool:
    return isinstance(fs, LocalFileSystem) and not fs.auto_mkdir


def is_default_fs(fs: fsspec.AbstractFileSystem) -> bool:
    return isinstance(fs, LocalFileSystem) and not fs.auto_mkdir
