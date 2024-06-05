import asyncio
from typing import List, Optional

from fastapi import APIRouter, Cookie, Path, Query, Response
from models.models import ApiResponse, NoteData
from services.fetch_datas import fetch_note_by_id, fetch_notes_data
from utils.response import resp_error, resp_success

router = APIRouter()


@router.get("/note/{note_id}", response_model=ApiResponse[NoteData])
async def get_note(
    note_id: str = Path(
        ..., title="Note ID", description="The ID of the note to retrieve"
    )
):
    """
    根据笔记ID获取笔记详情。

    Args:
        note_id (str): 需要获取的笔记的ID。

    Returns:
        NoteData: 笔记详情。

    示例:
        `http://localhost/note/xxx`
    """
    try:
        print("note id: ", note_id)
        data = await fetch_note_by_id(note_id)
        if data is None:
            return resp_error(msg="fetch note error")
        else:
            return resp_success(msg="fetch note success", data=data)
    except Exception as e:
        return resp_error(f"fetch note error: {str(e)}")


@router.get("/notes", response_model=ApiResponse[List[NoteData]])
async def get_notes(
    page: int = Query(1, alias="page"),
    limit: int = Query(10, alias="limit"),
    username: Optional[str] = Cookie(None),
    last_refresh: Optional[str] = Cookie(None),
):
    """
    分页查询笔记。

    通过指定页码（page）和每页数量（limit）来获取笔记列表的分页结果。
    本接口支持通过查询参数`page`和`limit`来控制分页信息，其中`page`默认为1，`limit`默认为10。

    Args:
        page (int): 请求的页码，用于计算分页查询的起始位置。
        limit (int): 每页展示的笔记数量，用于限制返回结果的数量。
        username (Optional[str]): 用户名，从Cookie中获取。默认为None。
        last_refresh (Optional[str]): 上次刷新时间，从Cookie中获取。默认为None。

    Returns:
        List[NoteData]: 笔记列表的分页查询结果。

    示例:
        `http://localhost/notes/?page=1&limit=10`
    """
    try:
        start = (page - 1) * limit
        end = start + limit
        datas = await fetch_notes_data(start=start, end=end, user_id=username)
        return resp_success("fetch notes success", datas)
    except Exception as e:
        return resp_error(f"fetch notes error: {str(e)}")
