from app.core.wechat.service import userAuth
from app.schemas.response.common import RestfulResponse
from fastapi import APIRouter

router = APIRouter()


@router.get("/wechat_auth")
def wechat_auth(code: str) -> RestfulResponse:
    if code == "":
        return RestfulResponse(code=-1, msg="code不能为空", data={})

    ret = userAuth(code)
    if ret != "":
        return RestfulResponse(code=-1, msg=ret, data={})

    return RestfulResponse(data={})
