from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sqlmodel import SQLModel, create_engine, Session, select

from tools.parse_file import parse_yaml

__all__ = ['engine', 'Session', 'SQLModel', "get_session", "Response", "select", "WHITE_LIST", "SUPPORT_METHOD"]

engine = create_engine('sqlite:///db.sqlite')

CONFIG = parse_yaml(Path('conf/config.yml'))
WHITE_LIST = CONFIG['white_list']
SUPPORT_METHOD = list(map(str.upper, CONFIG['support_method']))


def get_session():
    with Session(engine) as session:
        yield session


@dataclass
class BaseResp:
    code: int
    msg: str


@dataclass
class Response(BaseResp):
    code: int = 0
    msg: str = "成功"
    data: Any = None
