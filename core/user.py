from fastapi import APIRouter, Depends

from conf import get_session, Session, Response, select
from model.User import User, UserSelect

router = APIRouter(prefix="/user", tags=["用户"])


@router.post('/select', response_model=Response, response_model_exclude_none=True)
async def get_user(user: UserSelect, session: Session = Depends(get_session)):
    if not user.id:
        return Response(code=-1, msg="请输入待查询的用户ID")
    statement = select(User).where(User.id == user.id)
    if user.name:
        statement = statement.where(User.name == user.name)
    if not (user := session.exec(statement).fetchall()):
        return Response(code=-1, msg="用户不存在")
    return Response(data=user)
