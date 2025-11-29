from fastapi import APIRouter, Depends

from conf import ResponseBody
from core.depends import get_user_service
from core.services.service_user import UserService

router = APIRouter(tags=["用户"])


@router.get("/user_list")
async def user_list(user_service: UserService = Depends(get_user_service)):
    """
    用户列表
    """
    return ResponseBody(data=user_service.user_list())
