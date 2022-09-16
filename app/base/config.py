import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str
    PROJECT_KEY: str  # 本地开发时需要配置deta的project key
    LOG_FILE: str = "/tmp/app.log"
    LOG_LEVEL: str = "debug"
    TIMEOUT: int = 10
    WECHAT_APP_ID: str
    WECHAT_SECRET: str

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()  # type: ignore


def getProjectKey() -> str:
    pk = os.getenv("DETA_PROJECT_KEY", "")
    if pk != "":
        return pk

    return settings.PROJECT_KEY
