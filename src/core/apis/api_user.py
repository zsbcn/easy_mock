from fastapi import APIRouter, Depends, Request

from conf import ResponseBody
from core.depends import get_user_service, get_redis_service
from core.services.service_redis import RedisService
from core.services.service_user import UserService

router = APIRouter(tags=["用户"])


@router.get("/user_list")
async def user_list(user_service: UserService = Depends(get_user_service)):
    """
    用户列表
    """
    return ResponseBody(data=user_service.user_list())


@router.get("/user_info")
async def user_info(request: Request,
                    user_service: UserService = Depends(get_user_service),
                    redis_service: RedisService = Depends(get_redis_service)):
    """
    用户信息
    """
    session_id = request.session.get("sessionId")
    user_id = await redis_service.get_str(f"session:{session_id}")
    return ResponseBody(data=user_service.get_user_info(user_id))
