from fastapi import APIRouter, Request, Depends

from conf import get_session, Session, Response
from model.User import User

router = APIRouter()


@router.post("/login", response_model=Response, response_model_exclude_none=True)
async def login(user: User, request: Request, session: Session = Depends(get_session)):
    # 简单的登录逻辑，把user_id存到session中，便于其他接口获取user_id
    user_info = session.get(User, user.id)
    if user_info.name == user.user_name:
        request.session["user_id"] = user_info.id
        return Response()
    else:
        return Response(code=-1, msg="登录失败")
