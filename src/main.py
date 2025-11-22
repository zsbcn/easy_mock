import json
import os
import re
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from loguru import logger
from starlette_session import SessionMiddleware

from conf import SQLModel, engine, WHITE_LIST, Session
from core import all_routers
from core.login import LoginConstants
from model.User import User

system_routes = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    启动前创建数据库
    :param app:
    :return:
    """
    global system_routes
    load_dotenv()
    system_routes = [route for route in app.routes if type(route) == APIRoute]
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
    global system_routes
    need_session = False
    # 判断接口请求是否是系统内部接口
    for router in system_routes:
        path = request.url.path
        if path != router.__getattribute__("path"):
            continue
        if need_session := any([re.match(r, path) for r in WHITE_LIST]):
            break
    # 如果是系统的接口请求，不在白名单内的检查session
    if need_session:
        current_session = request.session
        if not current_session:
            code, msg = LoginConstants.USER_NOT_LOGIN
            return Response(content=json.dumps({"code": code, "msg": msg}, ensure_ascii=False), status_code=200,
                            media_type="application/json")
        user_id = current_session.get("userId")
        with Session(engine) as session:
            user = session.get(User, user_id)
        if not user:
            code, msg = LoginConstants.USER_NOT_EXIST
            return Response(content=json.dumps({"code": code, "msg": msg}, ensure_ascii=False), status_code=200,
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
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"), cookie_name="sessionId", max_age=3600)

if __name__ == '__main__':
    from uvicorn import run

    run(app, host="0.0.0.0", port=8000, log_level="error")
