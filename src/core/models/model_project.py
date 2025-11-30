from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from conf import DbBase, get_uuid, get_now_str


class Project(DbBase):
    """
    项目表
    """
    __tablename__ = "t_sys_projects"
    id: Mapped[str] = mapped_column(String(32), default=get_uuid, primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=1)
    create_at: Mapped[str] = mapped_column(String(16), default=get_now_str)
    update_at: Mapped[str] = mapped_column(String(16), default=get_now_str)
    create_by: Mapped[str] = mapped_column(String(32), nullable=False)


class ProjectCreate(BaseModel):
    """
    项目创建模型
    """
    name: str


class ProjectSelect(BaseModel):
    """
    项目查询模型
    """
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class ProjectResponse(BaseModel):
    """
    项目返回模型
    """
    id: str
    name: str
    status: int
    create_at: str
    update_at: str
    create_by: str

    model_config = ConfigDict(from_attributes=True)
