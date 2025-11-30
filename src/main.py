import os
import re
from contextlib import asynccontextmanager
from traceback import extract_tb

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from loguru import logger
from starlette.middleware.sessions import SessionMiddleware
from uvicorn import run

from conf import engine, settings, DbBase
from core.apis import all_routers
from core.constants import LoginConstants
from core.depends import get_redis_service
from core.exception import BusinessException

system_route_paths = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    启动前创建数据库
    :param app:
    :return:
    """
    global system_route_paths
    load_dotenv()
    system_route_paths = [getattr(route, "path") for route in app.routes if type(route) == APIRoute]
    DbBase.metadata.create_all(engine)
    logger.info("setup complete")
    yield


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def check_user(request: Request, call_next):
    """
    检查是否需要校验用户登录状态的中间件
    :param request:
    :param call_next:
    :return:
    """
    global system_route_paths
    need_session = False
    # 判断接口请求是否是系统内部接口
    path = request.url.path
    if path in system_route_paths and not any([re.match(r, path) for r in settings.white_list]):
        need_session = True
    # 如果是系统的接口请求，不在白名单内的检查session
    if need_session:
        session_id = request.session.get("sessionId")
        if not session_id:
            return JSONResponse(content=LoginConstants.NOT_LOGIN.as_dict())
        user_id = await get_redis_service().get_str(f"session:{session_id}")
        if not user_id:
            return JSONResponse(content=LoginConstants.NOT_LOGIN.as_dict())
    response: Response = await call_next(request)
    return response


@app.exception_handler(BusinessException)
async def business_exception_handler(request: Request, exc: BusinessException):
    """
    业务异常处理
    :param request:
    :param exc:
    :return:
    """
    frames = extract_tb(exc.__traceback__)
    exception = ["\nTraceback (most recent call last):"]
    for frame in frames:
        if ".venv" in frame.filename:
            continue
        exception.append(f"\nFile \"{frame.filename}\", line {frame.lineno}, in {frame.name}\n\t{frame.line}")
    logger.error("".join(exception))
    return JSONResponse(content=exc.as_dict())


# 加载所有路由
app.include_router(all_routers)

# 添加session的中间件
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"), session_cookie="sessionId", max_age=3600,
                   https_only=True)

if __name__ == '__main__':
    run(app, **settings.server.model_dump())
