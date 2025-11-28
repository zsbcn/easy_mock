from datetime import datetime
from pathlib import Path
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict, PydanticBaseSettingsSource, YamlConfigSettingsSource
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, DeclarativeBase

__all__ = ['engine', 'Session', "get_session", "ResponseBody", "settings", "DbBase", "get_uuid", "get_now_str",
           "RedisConfig"]


class DbBase(DeclarativeBase):
    """
    数据库模型基类
    """
    pass


def get_uuid() -> str:
    return uuid4().hex


def get_now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class Server(BaseModel):
    """
    服务器配置类
    """
    host: str
    port: int
    log_level: Literal["debug", "info", "warning", "error", "critical"]
    ssl_keyfile: str
    ssl_certfile: str


class DbConfig(BaseModel):
    """
    数据库配置类
    """
    url: str
    echo: bool = False
    connect_args: dict | None = None


class RedisConfig(BaseModel):
    """
    redis配置类
    """
    host: str = "127.0.0.1"
    port: int = 6379
    db: int = 0
    password: str | None = None
    prefix: str | None = None


class Settings(BaseSettings):
    """
    pydantic的配置类
    """
    server: Server
    db: DbConfig
    redis: RedisConfig
    white_list: list

    model_config = SettingsConfigDict(
        extra="ignore"
    )

    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls: type[BaseSettings],
            init_settings: PydanticBaseSettingsSource,
            env_settings: PydanticBaseSettingsSource,
            dotenv_settings: PydanticBaseSettingsSource,
            file_secret_settings: PydanticBaseSettingsSource,
    ):
        return (
            init_settings,
            YamlConfigSettingsSource(settings_cls, yaml_file=Path(__file__).parent / "config.yml",
                                     yaml_file_encoding="utf-8")
        )


settings = Settings()
engine = create_engine(**settings.db.model_dump())


def get_session():
    with Session(engine) as session:
        yield session


class ResponseBody(BaseModel):
    """
    管理接口响应类
    """
    code: str
    message: str
    data: Any | None = Field(default=None, exclude_if=lambda v: v is None)  # 值为None时不序列化
