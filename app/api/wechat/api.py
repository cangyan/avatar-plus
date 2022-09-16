import xml.etree.ElementTree as ET
from email import message

from app.base.logger import logger
from app.core.wechat.service import getAuthLink, isUserAuthed
from fastapi import APIRouter, Request
from fastapi.responses import PlainTextResponse, Response
from wechatpy import parse_message
from wechatpy.replies import TextReply

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

        reply = TextReply(content="输入'国庆快乐'可生成头像", message=msg)
        return Response(content=reply.__str__(), media_type="application/xml")
    # 默认
    return Response()
