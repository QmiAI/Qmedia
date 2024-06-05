import datetime
from typing import Annotated, Optional, Union

from fastapi import APIRouter, Cookie, Request, Response
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/set-cookie")
def set_cookie(response: Response):
    response.set_cookie(key="user_id", value="some_unique_value")
    return {"message": "Cookie has been set"}


@router.get("/get-cookie")
def get_cookie(user_id: str = Cookie(None)):
    print(user_id)
    return {"user_id": user_id}


@router.get("/get-user-agent")
async def get_user_agent(request: Request):
    user_agent = request.headers.get("User-Agent")
    print(user_agent)
    return {
        "User-Agent": user_agent,
        "header": request.headers,
        "req": request.cookies.get("sessionKey"),
    }


@router.get("/cookie/")
def login():
    content = {"message": "set cookie"}
    response = JSONResponse(content=content)
    # 设置用户名cookie
    response.set_cookie(key="username", value="zlkt")
    # 设置刷新标识cookie，记录当前时间戳
    response.set_cookie(
        key="last_refresh", value=str(datetime.datetime.now().timestamp())
    )
    return response


@router.get("/items/")
async def read_items(
    username: Optional[str] = Cookie(None), last_refresh: Optional[str] = Cookie(None)
):
    # 判断是否刷新的逻辑，这里简单地返回上次刷新时间
    if last_refresh:
        last_refresh_time = datetime.datetime.fromtimestamp(float(last_refresh))
        refreshed = last_refresh_time
    else:
        refreshed = "No refresh recorded."
    return {"name": username, "refreshed": refreshed}


@router.get("/set-username-cookie/")
def set_username_cookie(response: Response, username: str = "default_user"):
    """
    单独设置用户名cookie。
    """
    response.set_cookie(key="username", value=username)
    return {"message": f"Username cookie for {username} set."}


@router.get("/set-refresh-cookie/")
def set_refresh_cookie(response: Response):
    """
    单独设置刷新标识cookie，记录当前时间戳。
    """
    response.set_cookie(
        key="last_refresh", value=str(datetime.datetime.now().timestamp())
    )
    return {"message": "Refresh cookie set."}


@router.get("/get-username-cookie/")
def get_username_cookie(username: Optional[str] = Cookie(None)):
    """
    获取用户名cookie。
    """
    if username is None:
        return {"message": "No username cookie found."}
    else:
        return {"username": username}


@router.get("/get-refresh-cookie/")
def get_refresh_cookie(last_refresh: Optional[str] = Cookie(None)):
    """
    获取上次刷新时间的cookie。
    """
    if last_refresh:
        last_refresh_time = datetime.datetime.fromtimestamp(float(last_refresh))
        refreshed = last_refresh_time
    else:
        refreshed = "No refresh recorded."
    return {"refreshed": refreshed}
