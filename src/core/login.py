from fastapi import APIRouter, Request, Depends

from src.conf import get_session, Session, ResponseBody
from src.model.User import User


class LoginConstants:
    USER_LOGOUT_SUCCESS = ("0", "用户登出成功")
    USER_LOGIN_SUCCESS = ("0", "用户登录成功")
    USER_LOGIN_FAILED = ("1001", "用户登录失败")
    USER_NOT_LOGIN = ("1002", "用户未登录")
    USER_NOT_EXIST = ("1003", "用户不存在")
    USER_PASSWORD_ERROR = ("1004", "用户密码错误")


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
