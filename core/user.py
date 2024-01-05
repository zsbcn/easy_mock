from fastapi import APIRouter, Depends, Request

from conf import get_session, Session, ResponseBody, select
from model.User import User, UserCreate, UserDelete, UserUpdate, UserSelect


class UserService:
    def __init__(self, request: Request, session: Session):
        self.request = request
        self.session = session
        self.user_id = request.session.get("userId")

    def create(self, user: UserCreate):
        # 检查用户是否已经存在
        statement = select(User).where(User.id == user.id)
        if self.session.exec(statement).fetchall():
            return -1, "用户已存在", None
        db_user = User.model_validate(user)
        self.session.add(db_user)
        self.session.commit()
        return 0, "创建成功", None

    def delete(self, user: UserDelete):
        statement = select(User).where(User.id == user.id)
        if user.name:
            statement = select(User).where(User.name == user.name)
        if not (db_user := self.session.exec(statement).first()):
            return -1, "用户不存在", None
        self.session.delete(db_user)
        self.session.commit()
        return 0, "删除成功", None

    def update(self, user: UserUpdate):
        db_user = self.session.get(User, user.id)
        if not db_user:
            return -1, "用户不存在", None
        db_user.name = user.name
        self.session.add(db_user)
        self.session.commit()
        return 0, "更新成功", None

    def select(self, user: UserSelect):
        if not user.id:
            user.id = self.user_id
        statement = select(User).where(User.id == user.id)
        if user.name:
            statement = statement.where(User.name == user.name)
        result = self.session.exec(statement).one()
        return 0, "查询成功", result


router = APIRouter(prefix="/user", tags=["用户"])


@router.post("/create", response_model=ResponseBody, response_model_exclude_none=True)
async def create_user(user: UserCreate, request: Request, session: Session = Depends(get_session)):
    code, msg, result = UserService(request, session).create(user)
    return ResponseBody(code=code, msg=msg, data=result)


@router.post("/delete", response_model=ResponseBody, response_model_exclude_none=True)
async def delete_user(user: UserDelete, request: Request, session: Session = Depends(get_session)):
    code, msg, result = UserService(request, session).delete(user)
    return ResponseBody(code=code, msg=msg, data=result)


@router.post("/update", response_model=ResponseBody, response_model_exclude_none=True)
async def update_user(user: UserUpdate, request: Request, session: Session = Depends(get_session)):
    code, msg, result = UserService(request, session).update(user)
    return ResponseBody(code=code, msg=msg, data=result)


@router.post("/select", response_model=ResponseBody, response_model_exclude_none=True)
async def select_user(user: UserSelect, request: Request, session: Session = Depends(get_session)):
    """
    用户信息查询接口
    :param user:
    :param request:
    :param session:
    :return:
    """
    code, msg, result = UserService(request, session).select(user)
    return ResponseBody(code=code, msg=msg, data=result)
