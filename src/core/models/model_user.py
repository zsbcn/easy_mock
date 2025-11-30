from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from conf import DbBase, get_now_str
from core.models.model_project import ProjectSelect


class User(DbBase):
    """
    用户表
    """
    __tablename__ = "t_sys_users"
    user_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    salt: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=1)  # 0: 无效; 1: 有效
    create_at: Mapped[str] = mapped_column(String(16), default=get_now_str)
    update_at: Mapped[str] = mapped_column(String(16), default=get_now_str)


class UserCreate(BaseModel):
    """
    用户创建模型
    """
    user_id: str
    username: str
    password: str


class UserLogin(UserCreate):
    """
    用户登录模型
    """
    user_id: str
    password: str


class UserResponse(BaseModel):
    """
    用户返回模型
    """
    user_id: str
    username: str
    status: int
    create_at: str
    update_at: str

    model_config = ConfigDict(from_attributes=True)


class UserInfo(BaseModel):
    """
    用户信息
    """
    user_id: str
    username: str
    status: int
    project_list: list[ProjectSelect] | None = None

    model_config = ConfigDict(from_attributes=True)
