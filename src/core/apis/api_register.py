from fastapi import APIRouter, Depends

from conf import ResponseBody
from core.constants import RegisterConstants
from core.depends import get_register_service
from core.models.model_user import UserCreate
from core.services.service_register import RegisterService

router = APIRouter(tags=["注册"])


@router.post("/register")
async def register(user: UserCreate, register_service: RegisterService = Depends(get_register_service)):
    # 创建用户
    register_service.register(user)
    return ResponseBody(**RegisterConstants.SUCCESS.as_dict())
