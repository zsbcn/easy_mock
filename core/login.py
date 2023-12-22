from dataclasses import dataclass

from fastapi import APIRouter, Request, Depends

from conf import get_session, Session, Response
from model.User import User

router = APIRouter()


@dataclass
class LoginReq:
    user_id: str
    user_name: str


@router.post("/login", response_model=Response, response_model_exclude_none=True)
async def login(request: Request, user: LoginReq, session: Session = Depends(get_session)):
    user_info = session.get(User, user.user_id)
    if user_info.name == user.user_name:
        request.session["user_id"] = user_info.id
        return Response()
    else:
        return Response(code=-1, msg="登录失败")
