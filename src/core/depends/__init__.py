from fastapi import Depends, Request

from conf import Session, get_session, settings
from core.constants import LoginConstants
from core.exception import BusinessException
from core.services.service_interface import InterfaceService
from core.services.service_login import LoginService
from core.services.service_project import ProjectService
from core.services.service_redis import RedisService
from core.services.service_register import RegisterService
from core.services.service_user import UserService


def get_register_service(db: Session = Depends(get_session)) -> RegisterService:
    return RegisterService(db)


def get_login_service(db: Session = Depends(get_session)) -> LoginService:
    return LoginService(db)


def get_redis_service() -> RedisService:
    return RedisService(settings.redis)


def get_user_service(db: Session = Depends(get_session)) -> UserService:
    return UserService(db)


def get_project_service(db: Session = Depends(get_session)) -> ProjectService:
    return ProjectService(db)


def get_interface_service(db: Session = Depends(get_session)) -> InterfaceService:
    return InterfaceService(db)


async def get_user_id(request: Request, redis_service: RedisService = Depends(get_redis_service)) -> str:
    session_id = request.session.get("sessionId")
    user_id = await redis_service.get_str(f"session:{session_id}")
    if not user_id:
        raise BusinessException(LoginConstants.NOT_LOGIN)
    return user_id
