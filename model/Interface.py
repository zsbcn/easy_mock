from typing import Optional

from conf import SQLModel, Field


class InterfaceBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    url: str = Field(min_length=1, max_length=100)
    method: str = Field(min_length=1, max_length=100)
    description: Optional[str] = None


class Interface(InterfaceBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = None


class InterfaceCreate(InterfaceBase):
    pass


class InterfaceDelete(InterfaceBase):
    id: Optional[int] = None
    user_id: Optional[str] = None


class InterfaceUpdate(InterfaceBase):
    id: Optional[int] = None
    user_id: Optional[str] = None


class InterfaceSelect(SQLModel):
    id: Optional[int] = None
