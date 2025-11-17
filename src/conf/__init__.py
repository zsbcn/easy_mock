from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlmodel import SQLModel, Field, create_engine, Session, select

from tools.parse_file import parse_yaml

__all__ = ['engine', 'Session', 'SQLModel', "Field", "get_session", "ResponseBody", "select", "CONFIG","WHITE_LIST",
           "SUPPORT_METHODS"]

sqlite_file_name = "db.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=False, connect_args=connect_args)

# 读取配置文件
CONFIG = parse_yaml(Path('conf/config.yml'))
WHITE_LIST = CONFIG['white_list']
SUPPORT_METHODS = [method["value"] for method in CONFIG['support_methods']]


def get_session():
    with Session(engine) as session:
        yield session


@dataclass
class ResponseBody:
    """
    管理接口响应类
    """
    code: str = "0"
    msg: str = "成功"
    data: Any = None
