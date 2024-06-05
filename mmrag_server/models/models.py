from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel, Field, HttpUrl

T = TypeVar("T")


class ImageData(BaseModel):
    id: Optional[str] = None
    note_id: Optional[str] = None
    image_urls: Optional[List[str]] = []
    image_ids: Optional[List[str]] = []


class VideoData(BaseModel):
    id: Optional[str] = None
    note_id: Optional[str] = None
    video_url: Optional[List[str]] = []
    video_ids: Optional[List[str]] = []


class UserDict(BaseModel):
    user_id: str
    nickname: str
    avatar: str


class InteractInfo(BaseModel):
    relation: str
    liked: bool
    liked_count: int
    collected: bool
    collected_count: int
    comment_count: int
    share_count: int
    followed: bool


class InfoData(BaseModel):
    id: str
    note_id: str
    model_type: str
    card_type: str
    title: str
    desc: str
    user_dict: UserDict
    interact_info: InteractInfo
    tag_list: List[str]


class NoteData(BaseModel):
    image_data: ImageData
    video_data: VideoData
    info_data: InfoData


class ApiResponse(BaseModel, Generic[T]):
    code: int = Field(
        ...,
        description="Response code, 0 means success, non-zero means different types of errors",
    )
    success: bool = Field(
        ..., description="Whether the request was successfully processed"
    )
    msg: str = Field(..., description="Response message or error description")
    data: Optional[T] = Field(None, description="Data returned when successful")
    error: Optional[str] = Field(
        None, description="Error message, only returned when an error occurs"
    )
