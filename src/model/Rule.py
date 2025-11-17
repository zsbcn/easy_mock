from typing import Optional

from src.conf import SQLModel, Field
from sqlmodel import UniqueConstraint, Relationship


class RuleBase(SQLModel):
    interface_id: int = Field(default=None, foreign_key="interface.id")
    name: str
    input_content: str
    request_media_type: str
    output_content: str
    response_media_type: str
    status_code: int


class Rule(RuleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: int = Field(default=True)
    interface: Optional["Interface"] = Relationship(back_populates="rules")
    __table_args__ = (UniqueConstraint("interface_id", "input_content", name="unique_rule"),)


class RuleCreate(RuleBase):
    pass


class RuleDelete(SQLModel):
    id: Optional[int] = None


class RuleUpdate(RuleBase):
    id: int


class RuleSelect(SQLModel):
    id: int = None
    interface_id: int = None
    input_content: str = None
    output_content: str = None
