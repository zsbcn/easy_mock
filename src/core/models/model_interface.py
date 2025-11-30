from typing import Literal

from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from conf import DbBase, get_uuid, get_now_str


class Interface(DbBase):
    """
    接口表
    """
    __tablename__ = "t_sys_interfaces"
    id: Mapped[str] = mapped_column(String(32), default=get_uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    method: Mapped[str] = mapped_column(String(8))
    url: Mapped[str] = mapped_column(String(128))
    status: Mapped[int] = mapped_column(Integer, default=1)  # 0: 无效; 1: 有效
    parent_id: Mapped[str] = mapped_column(String(32), nullable=False)
    project_id: Mapped[str] = mapped_column(String(32), nullable=False)
    data_type: Mapped[int] = mapped_column(Integer, default=1)  # 0: 接口; 1: 目录
    create_at: Mapped[str] = mapped_column(String(16), default=get_now_str)
    create_by: Mapped[str] = mapped_column(String(32), nullable=False)
    update_at: Mapped[str] = mapped_column(String(16), default=get_now_str)
    update_by: Mapped[str] = mapped_column(String(32), nullable=False)


class InterfaceCreate(BaseModel):
    """
    接口创建模型
    """
    project_id: str  # 项目id
    data_type: Literal[0, 1]  # 0: 接口; 1: 目录
    parent_id: str = "-1"  # 默认是根目录
    name: str
    method: str | None = None
    url: str | None = None


class InterfaceResponse(BaseModel):
    """
    接口返回模型
    """
    id: str
    name: str
    method: str | None
    url: str | None
    status: int
    parent_id: str
    project_id: str
    data_type: int
    create_by: str
    update_by: str

    model_config = ConfigDict(from_attributes=True)
