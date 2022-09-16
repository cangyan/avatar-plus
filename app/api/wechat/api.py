import urllib.request

from app.base.logger import logger
from app.core.image.service import mergeImage
from app.core.wechat.service import (
    getAuthLink,
    getUserAvatar,
    isUserAuthed,
    uploadAvatar,
)
from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, Response
from wechatpy import parse_message
from wechatpy.replies import ImageReply, TextReply

router = APIRouter()


@router.get("/message")
def get_message(
    signature: str, echostr: str, timestamp: int, nonce: str
) -> PlainTextResponse:
    return PlainTextResponse(content=echostr)


@router.post("/message")
async def post_message(request: Request) -> Response:
    body = await request.body()
    msg = parse_message(body)

    logger.debug(msg)
    assert msg is not None
    type = msg.type
    if type == "event":  # 订阅事件
        event = msg.event
        if event == "subscribe":
            welcomeTips = """欢迎关注蒙德伊彼公众号。输入'国庆快乐'可生成头像"""
            reply = TextReply(content=welcomeTips, message=msg)
            return Response(
                content=reply.__str__(), media_type="application/xml"
            )
    elif type == "text":  # 文本消息
        content = msg.content
        if content == "国庆快乐":
            # 判断是否授权
            if isUserAuthed(str(msg.source)) != True:
                # 未授权提示授权信息
                authTips = """点击链接授权{link}"""
                reply = TextReply(
                    content=authTips.format(link=getAuthLink()), message=msg
                )
                return Response(
                    content=reply.__str__(), media_type="application/xml"
                )

            # 获取用户头像
            avatar_link, errmsg = getUserAvatar(str(msg.source))
            if errmsg != "":
                reply = TextReply(content=errmsg, message=msg)
                return Response(
                    content=reply.__str__(), media_type="application/xml"
                )

            logger.debug(avatar_link)
            # 合成头像
            req = urllib.request.urlopen(avatar_link)
            base64Img = mergeImage(req.read())
            # 上传临时素材
            media_id = uploadAvatar(base64Img)
            # 回复
            reply = ImageReply(media_id=media_id, message=msg)
            return Response(
                content=reply.__str__(), media_type="application/xml"
            )

        reply = TextReply(content="输入'国庆快乐'可生成头像", message=msg)
        return Response(content=reply.__str__(), media_type="application/xml")
    # 默认
    return Response()
