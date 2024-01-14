from typing import Optional, List
from sqlmodel import Relationship
from conf import SQLModel, Field
from model.Rule import Rule


class InterfaceBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    url: str = Field(min_length=1, max_length=100)
    method: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(nullable=True)


class Interface(InterfaceBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(default=None, foreign_key="user.id")
    status: int = Field(default=True)
    rules: Optional[List[Rule]] = Relationship(back_populates="interface")


class InterfaceCreate(InterfaceBase):
    pass


class InterfaceDelete(SQLModel):
    id: List[int]


class InterfaceUpdate(InterfaceBase):
    id: int


class InterfaceSelect(SQLModel):
    id: int = None
    name: str = None
    url: str = None
    method: str = None


class InterfaceStatus(SQLModel):
    id: int
    status: int


class InterfaceResponse(SQLModel):
    id: int
    name: str
    url: str
    method: str
    description: str
    status: int
    rules: Optional[List[Rule]]
