from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from models.models import ApiResponse


async def http_exception_handler(request: Request, exc: HTTPException):
    response_content = ApiResponse(
        code=exc.status_code, success=False, msg="error", error=exc.detail
    )
    return JSONResponse(
        status_code=exc.status_code, content=response_content.model_dump_json()
    )
