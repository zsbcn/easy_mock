from conf import SQLModel, Field


class UserBase(SQLModel):
    id: str
    name: str = None


class User(SQLModel, table=True):
    id: str = Field(primary_key=True, max_length=32)
    name: str = Field(max_length=64, nullable=True)


class UserCreate(UserBase):
    pass


class UserDelete(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserSelect(UserBase):
    pass
