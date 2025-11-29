from pydantic import BaseModel, ConfigDict
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from conf import DbBase, get_uuid, get_now_str


class User(DbBase):
    """
    用户表
    """
    __tablename__ = "t_sys_users"
    id: Mapped[str] = mapped_column(String(32), default=get_uuid, primary_key=True)
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    password: Mapped[str] = mapped_column(String(64), nullable=False)
    salt: Mapped[str] = mapped_column(String(32), nullable=False)
    status: Mapped[int] = mapped_column(Integer, default=1)
    create_at: Mapped[str] = mapped_column(String(16), default=get_now_str)
    update_at: Mapped[str] = mapped_column(String(16), default=get_now_str)


class UserCreate(BaseModel):
    """
    用户创建模型
    """
    username: str
    password: str


class UserLogin(UserCreate):
    """
    用户登录模型
    """
    pass


class UserResponse(BaseModel):
    """
    用户返回模型
    """
    id: str
    username: str
    status: int
    create_at: str
    update_at: str

    model_config = ConfigDict(from_attributes=True)
