from typing import Optional

from conf import SQLModel, Field


class InterfaceBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    url: str = Field(min_length=1, max_length=100)
    method: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(nullable=True)


class Interface(InterfaceBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = None


class InterfaceCreate(InterfaceBase):
    pass


class InterfaceDelete(SQLModel):
    id: int


class InterfaceUpdate(InterfaceBase):
    id: int


class InterfaceSelect(SQLModel):
    id: int = None
    name: str = None
    url: str = None
    method: str = None
