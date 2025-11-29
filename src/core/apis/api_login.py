from secrets import token_hex

from fastapi import APIRouter, Depends, Request

from conf import ResponseBody
from core.constants import LoginConstants, LogoutConstants
from core.depends import get_login_service, get_redis_service
from core.models.model_user import UserLogin
from core.services.service_login import LoginService
from core.services.service_redis import RedisService

router = APIRouter(tags=["登录"])


@router.post("/login")
async def login(user: UserLogin, request: Request, login_service: LoginService = Depends(get_login_service),
                redis_service: RedisService = Depends(get_redis_service)):
    # 创建用户
    login_service.login(user)
    session_id = token_hex(16)
    request.session["sessionId"] = session_id
    await redis_service.set_add_with_expires(f"session:{session_id}", user.username, 3600)
    return ResponseBody(**LoginConstants.SUCCESS.as_dict())


@router.post("/logout")
async def logout(request: Request, redis_service: RedisService = Depends(get_redis_service)):
    # 退出登录，清空session
    session_id = request.session.get("sessionId")
    request.session.pop("sessionId", None)
    await redis_service.delete_set(f"session:{session_id}")
    return ResponseBody(**LogoutConstants.SUCCESS.as_dict())
