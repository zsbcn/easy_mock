import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from starlette.middleware.sessions import SessionMiddleware

from conf import SQLModel, engine, WHITE_LIST, Session
from core import all_routers
from model.User import User
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    logger.info("setup complete")
    yield


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def check_user(request: Request, call_next):
    if request.url.path not in WHITE_LIST:
        current_session = request.session
        if not current_session:
            return Response(content=json.dumps({"code": -1, "msg": "请先登录"}), status_code=200,
                            media_type="application/json")
        user_id = current_session.get("user_id")
        with Session(engine) as session:
            user = session.get(User, user_id)
        if not user:
            return Response(content=json.dumps({"code": -1, "msg": "请先在系统在注册后，再登录"}), status_code=200,
                            media_type="application/json")
    response = await call_next(request)
    return response


app.include_router(all_routers)
app.add_middleware(SessionMiddleware, secret_key="123456", max_age=3600)
