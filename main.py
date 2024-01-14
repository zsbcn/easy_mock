import json
import re
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette_session import SessionMiddleware

from conf import SQLModel, engine, WHITE_LIST, Session
from core import all_routers
from core.login import LoginConstants
from model.User import User


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    启动前创建数据库
    :param app:
    :return:
    """
    SQLModel.metadata.create_all(engine)
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
    system_path = False
    need_session = True
    # 判断接口请求是否是系统内部接口
    for router in app.routes:
        if request.url.path == router.__getattribute__("path"):
            system_path = True
            break
    if system_path:
        for r in WHITE_LIST:
            if re.match(r, request.url.path):
                need_session = False
                break
    # 如果是系统的接口请求，不在白名单内的检查session
    if system_path and need_session:
        current_session = request.session
        if not current_session:
            code, msg = LoginConstants.USER_NOT_LOGIN
            return Response(content=json.dumps({"code": code, "msg": msg}), status_code=200,
                            media_type="application/json")
        user_id = current_session.get("userId")
        with Session(engine) as session:
            user = session.get(User, user_id)
        if not user:
            code, msg = LoginConstants.USER_NOT_EXIST
            return Response(content=json.dumps({"code": code, "msg": msg}), status_code=200,
                            media_type="application/json")
    response: Response = await call_next(request)
    return response


# 加载所有路由
app.include_router(all_routers)

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 添加session的中间件
app.add_middleware(SessionMiddleware, secret_key="xxxxxx", cookie_name="sessionId", max_age=3600)
