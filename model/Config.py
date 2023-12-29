from conf import SQLModel, Field


class Config(SQLModel, table=True):
    id: str = Field(primary_key=True)
    group: str
    key: str
    value: str


class ConfigResp(SQLModel):
    key: str
    value: str
