import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from starlette_session import SessionMiddleware

from conf import SQLModel, engine, WHITE_LIST, Session
from conf.constants import LoginConstants
from core import all_routers
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


@app.middleware("http")
async def check_user(request: Request, call_next):
    """
    检查是否需要校验用户登录状态的中间件
    :param request:
    :param call_next:
    :return:
    """
    if request.url.path not in WHITE_LIST:
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
    response = await call_next(request)
    return response


# 加载所有路由
app.include_router(all_routers)
# 添加session的中间件
app.add_middleware(SessionMiddleware, secret_key="xxxxxx", cookie_name="sessionId", max_age=3600)
