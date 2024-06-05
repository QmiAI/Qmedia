from models.models import ApiResponse


def resp_success(msg: str, data, code=0):
    return ApiResponse(code=code, success=True, msg=msg, data=data)


def resp_error(msg: str):
    return ApiResponse(code=-1, success=False, msg=msg)
