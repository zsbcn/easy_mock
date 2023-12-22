from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlmodel import SQLModel, Field, create_engine, Session, select

from tools.parse_file import parse_yaml

__all__ = ['engine', 'Session', 'SQLModel', "Field", "get_session", "Response", "select", "WHITE_LIST",
           "SUPPORT_METHOD"]

engine = create_engine('sqlite:///db.sqlite')  # 数据库

# 读取配置文件
CONFIG = parse_yaml(Path('conf/config.yml'))
WHITE_LIST = CONFIG['white_list']
SUPPORT_METHOD = list(map(str.upper, CONFIG['support_method']))


def get_session():
    with Session(engine) as session:
        yield session


@dataclass
class Response:
    """
    管理接口响应类
    """
    code: int = 0
    msg: str = "成功"
    data: Any = None
