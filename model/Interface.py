from typing import Optional

from conf import SQLModel, Field


class InterfaceBase(SQLModel):
    id: int = None
    name: str = None
    url: str = None
    method: str = None
    description: str = None


class Interface(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(default=None, nullable=True)
    url: str = Field(default=None, nullable=True)
    method: str = Field(default=None, nullable=True)
    description: str = Field(nullable=True)
    user_id: str


class InterfaceCreate(InterfaceBase):
    pass


class InterfaceDelete(SQLModel):
    pass


class InterfaceUpdate(InterfaceBase):
    pass


class InterfaceSelect(SQLModel):
    pass
