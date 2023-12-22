from fastapi import APIRouter, Depends, Request

from conf import get_session, Session, Response, select
from model.User import User

router = APIRouter(prefix="/user", tags=["用户"])


@router.post('/select', response_model=Response, response_model_exclude_none=True)
async def get_user(request: Request, session: Session = Depends(get_session)):
    """
    用户信息查询接口
    :param request:
    :param session:
    :return:
    """
    user_id = request.session.get("user_id")
    statement = select(User).where(User.id == user_id)
    if not (user := session.exec(statement).fetchall()):
        return Response(code=-1, msg="用户不存在")
    return Response(data=user)
