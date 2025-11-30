from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from conf import DbBase


class UserProject(DbBase):
    """
    用户项目表
    """
    __tablename__ = "t_user_projects"
    user_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    project_id: Mapped[str] = mapped_column(String(64), primary_key=True)
