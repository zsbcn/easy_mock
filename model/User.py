from conf import SQLModel, Field


class UserBase(SQLModel):
    id: str = Field(primary_key=True, max_length=32)
    name: str = Field(max_length=64, nullable=True)


class User(UserBase, table=True):
    pass


class UserCreate(UserBase):
    pass


class UserSelect(UserBase):
    pass
