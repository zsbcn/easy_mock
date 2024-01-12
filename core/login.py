from fastapi import APIRouter, Request, Depends

from conf import get_session, Session, ResponseBody
from model.User import User
from conf.constants import LoginConstants

router = APIRouter(tags=["登录"])


@router.post("/login", response_model=ResponseBody, response_model_exclude_none=True)
async def login(user: User, request: Request, db_session: Session = Depends(get_session)):
    # 简单的登录逻辑，把userId存到session中，便于其他接口获取userId
    user_info = db_session.get(User, user.id)
    if not user_info:
        return ResponseBody(*LoginConstants.USER_NOT_EXIST)
    elif user_info.name == user.name:
        request.session["userId"] = user_info.id
        return ResponseBody(*LoginConstants.USER_LOGIN_SUCCESS)
    else:
        return ResponseBody(*LoginConstants.USER_LOGIN_FAILED)


@router.post("/logout", response_model=ResponseBody, response_model_exclude_none=True)
async def logout(request: Request):
    # 退出登录，清空session
    request.session.pop("userId", None)
    return ResponseBody(*LoginConstants.USER_LOGOUT_SUCCESS)
