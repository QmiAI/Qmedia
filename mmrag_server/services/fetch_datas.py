import json
from datetime import datetime
from typing import Dict, List, Optional

from config import Config
from fastapi import APIRouter, HTTPException, Query
from models.models import ImageData, NoteData, VideoData
from utils.http_utils import merge_path, merge_url
from utils.response import resp_error

json_file_path = Config.json_file_path
with open(json_file_path, "r", encoding="utf-8") as f:
    _datas: List[NoteData] = json.load(f)

datas: List[NoteData] = []
for _data in _datas:
    datas.append(NoteData.model_validate(_data))

for _data in datas:
    # process image
    urls = _data.image_data.image_urls
    _data.image_data.image_ids = urls
    _data.image_data.image_urls = [merge_path(Config.store_host, i) for i in urls]

    # process video
    urls = _data.video_data.video_url
    _data.video_data.video_ids = urls
    _data.video_data.video_url = [merge_path(Config.store_host, i) for i in urls]


kvdatas: Dict[str, NoteData] = {
    note_data.info_data.note_id: note_data for note_data in datas
}

user_history = {}
DEFAULT_NOTES = 10


def generate_user_specific_notes(user_id: str, number_of_notes: int) -> List[NoteData]:
    """
    根据用户特性生成指定数量的“猜你喜欢”的数据列表。
    """
    # 此处简化，实际应根据用户特性动态生成
    number_notes = min(len(datas), number_of_notes)
    notes = datas[0:number_notes]
    return notes


async def fetch_notes_data(start: int, end: int, user_id: str) -> List[NoteData]:
    """
    # 1. 如果是首页, 根据用户特性猜你喜欢, 得到数据列表
    # 2. 如果页数超过数据列表, 重新进行猜你喜欢
    # 3. 缓存用户历史数据, 可以回退.
    获取笔记数据，包括生成“猜你喜欢”的数据和处理页数超出的情况。
    """
    # print(user_history)
    if user_id is None:
        return generate_user_specific_notes(user_id, max(end, DEFAULT_NOTES))

    if user_id not in user_history or start == 1:
        # 如果用户ID不存在于历史中或请求的是首页，重置用户数据
        user_history[user_id] = {
            "notes": generate_user_specific_notes(user_id, max(end, DEFAULT_NOTES)),
            "refresh_timestamp": datetime.now().timestamp(),
        }
    else:
        current_data = user_history[user_id]["notes"]
        current_number_of_notes = len(current_data)
        if end > current_number_of_notes:
            # 如果请求的数据超出当前数据量，生成并追加新的数据
            additional_notes_needed = max(end - current_number_of_notes, DEFAULT_NOTES)
            new_notes = generate_user_specific_notes(user_id, additional_notes_needed)
            user_history[user_id]["notes"].extend(new_notes)

    # 返回用户请求的数据范围
    try:
        return user_history[user_id]["notes"][start:end]
    except Exception as e:
        raise RuntimeError(f"Error fetch_notes_data {str(e)}")


async def fetch_note_by_id(id: str) -> Optional[NoteData]:
    return kvdatas.get(id, None)


async def fetch_notes_by_search(query: str) -> List[NoteData]:
    start = 0
    end = 10
    return datas[start:end]


def deduplicated_nodes(nodes: List[NoteData]) -> List[NoteData]:
    seen_ids = set()
    deduplicated_results = []

    for item in nodes:
        node = item.node
        if node.node_id not in seen_ids:
            deduplicated_results.append(item)
            seen_ids.add(node.node_id)
    return deduplicated_results
