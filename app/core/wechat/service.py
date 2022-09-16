from app.base.config import settings
from wechatpy.client import WeChatClient
from wechatpy.session import SessionStorage


class CustomStorage(SessionStorage):
    def __init__(self, *args, **kwargs):
        self.cache = dict()

    def get(self, key, default=None):
        print("get_key", key)
        return self.cache.get(key, None)

    def set(self, key, value, ttl=None):
        print("set_key", key, value)
        self.cache[key] = value
        return

    def delete(self, key):
        self.cache.pop(key)
        return


wechat_client = WeChatClient(
    settings.WECHAT_APP_ID, settings.WECHAT_SECRET, session=CustomStorage()
)
