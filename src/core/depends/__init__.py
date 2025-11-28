from fastapi import Depends

from conf import Session, get_session, settings
from core.services.service_login import LoginService
from core.services.service_redis import RedisService
from core.services.service_register import RegisterService


def get_register_service(db: Session = Depends(get_session)):
    return RegisterService(db)


def get_login_service(db: Session = Depends(get_session)) -> LoginService:
    return LoginService(db)


def get_redis_service():
    return RedisService(settings.redis)
