import asyncio
from typing import List

from config import Config
from fastapi import APIRouter, Query
from models.models import ApiResponse, NoteData
from services.fetch_datas import fetch_notes_by_search
from services.search.google_search import (
    OutreachSearchResult,
    get_google_search,
    get_search_template,
)
from utils.response import resp_error, resp_success

router = APIRouter()


@router.get("/note-search", response_model=ApiResponse[List[NoteData]])
async def search_notes(query: str = Query(None, alias="query")):
    """
    Args:
        query (str): 搜索查询字符串，用于过滤笔记。

    Returns:
        List[NoteData]: 笔记列表的搜索结果。

    示例URL:
        http://127.0.0.1:8000/search/?query=Python

    """

    try:
        datas = await fetch_notes_by_search(query)
        return resp_success("Search qa success", datas)
    except:
        return resp_error("Note search error")


@router.get("/public-search", response_model=ApiResponse[List[OutreachSearchResult]])
async def search_public(
    query: str = Query(None, alias="query"),
    max_search: int = Query(3, alias="max_search"),
):
    """
    Args:
        query (str): 搜索查询字符串。
        max_search (int): 搜索结果的最大数量。
        `http://localhost:8001/public-search?query=如何拍摄Vlog&max_search=3`

    """
    try:
        if Config.use_google_search:
            datas: List[OutreachSearchResult] = await get_google_search(
                query, max_search
            )
        else:
            datas: List[OutreachSearchResult] = await get_search_template(
                query, max_search
            )
        return resp_success("Search outreach success", datas)
    except:
        return resp_error("public Search error")
