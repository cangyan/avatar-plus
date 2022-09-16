import json
import urllib.parse

import requests
from app.base.config import settings
from app.base.logger import logger
from wechatpy.client import WeChatClient
from wechatpy.session import SessionStorage


class CustomStorage(SessionStorage):
    def __init__(self, *args, **kwargs):
        self.cache = dict()

    def get(self, key, default=None):
        # print("get_key", key)
        return self.cache.get(key, None)

    def set(self, key, value, ttl=None):
        # print("set_key", key, value)
        self.cache[key] = value
        return

    def delete(self, key):
        self.cache.pop(key)
        return


storage = CustomStorage()

wechat_client = WeChatClient(
    settings.WECHAT_APP_ID, settings.WECHAT_SECRET, session=storage
)


def getAuthLink() -> str:
    url = "https://open.weixin.qq.com/connect/oauth2/authorize"
    params = {
        "appId": settings.WECHAT_APP_ID,
        "redirect_uri": "http://deta.ngrok.huuinn.com/web/wechat_auth",
        "response_type": "code",
        "scope": "snsapi_userinfo",
        "state": "STATE",
    }

    q = urllib.parse.urlencode(params)
    return url + "?" + q + "#wechat_redirect"


def userAuth(code: str) -> str:
    url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code".format(
        settings.WECHAT_APP_ID, settings.WECHAT_SECRET, code
    )

    response = requests.request("GET", url)

    ret = json.loads(response.text)

    ret_code = ret.get("errcode", 0)
    if ret_code != 0:
        return ret.get("errmsg")
    storage.set(ret.get("openid"), ret.get("access_token"))

    logger.info("{}设置token成功".format(ret.get("openid")))
    return ""


def isUserAuthed(user: str) -> bool:
    return storage.get(user, None) != None


def setUserAccessToken(user: str, at: str) -> None:
    return storage.set(user, at)


def getUserAccessToken(user: str) -> str:
    return str(storage.get(user))


def delUserAccessToken(user: str) -> None:
    return storage.delete(user)


def getUserAvatar(user: str) -> str:
    return ""  # base64


def uploadAvatar(image: str) -> str:
    return ""  # media_id
