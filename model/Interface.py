from typing import Optional

from sqlmodel import SQLModel, Field


class InterfaceBase(SQLModel):
    name: str
    url: str
    method: str
    description: str = Field(nullable=True)


class Interface(InterfaceBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str


class InterfaceCreate(InterfaceBase):
    user_id: Optional[str] = None


class InterfaceDelete(SQLModel):
    id: str


class InterfaceUpdate(InterfaceBase):
    id: str


class InterfaceSelect(SQLModel):
    id: str
