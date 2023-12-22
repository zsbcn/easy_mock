from typing import Optional

from sqlmodel import SQLModel, Field


class RuleBase(SQLModel):
    interface_id: str
    input_content: str
    output_content: str
    response_media_type: str
    status_code: int


class Rule(RuleBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class RuleCreate(RuleBase):
    pass


class RuleDelete(SQLModel):
    id: Optional[str] = None
    interface_id: str


class RuleUpdate(RuleBase):
    id: str


class RuleSelect(SQLModel):
    id: Optional[str] = None
    interface_id: Optional[str] = None
