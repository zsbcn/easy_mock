from fastapi import APIRouter, Request, Depends

from conf import get_session, Session, ResponseBody
from model.User import User

router = APIRouter(tags=["登录"])


@router.post("/login", response_model=ResponseBody, response_model_exclude_none=True)
async def login(user: User, request: Request, session: Session = Depends(get_session)):
    # 简单的登录逻辑，把user_id存到session中，便于其他接口获取user_id
    user_info = session.get(User, user.id)
    if not user_info:
        return ResponseBody(code=-1, msg="用户不存在")
    elif user_info.name == user.name:
        request.session["userId"] = user_info.id
        return ResponseBody(code=0, msg="登录成功")
    else:
        return ResponseBody(code=-1, msg="登录失败")
