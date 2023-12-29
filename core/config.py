from fastapi import APIRouter, Depends

from conf import get_session, Session, Response, select
from model.Config import Config, ConfigResp

router = APIRouter(prefix="/config", tags=["系统配置"])


@router.get("/get", response_model=Response, response_model_exclude_none=True)
async def get_name(group: str, key: str = None, session: Session = Depends(get_session)):
    statement = select(Config).where(Config.group == group)
    if key:
        statement = statement.where(Config.key == key)
    result = session.exec(statement).fetchall()
    response_data = []
    for i in result:
        response_data.append(ConfigResp(key=i.key, value=i.value))
    return Response(data=response_data)
