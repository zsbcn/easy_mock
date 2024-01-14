from fastapi import APIRouter, Depends, Request

from conf import get_session, Session, ResponseBody, select
from model.User import User, UserCreate, UserDelete, UserUpdate, UserSelect
from sqlalchemy.exc import NoResultFound


class UserService:
    def __init__(self, request: Request, db_session: Session):
        self.request = request
        self.db_session = db_session
        self.user_id = request.session.get("userId")

    def create(self, user: UserCreate):
        # 检查用户是否已经存在
        statement = select(User).where(User.id == user.id)
        if self.db_session.exec(statement).fetchall():
            return -1, "用户已存在", None
        db_user = User.model_validate(user)
        self.db_session.add(db_user)
        self.db_session.commit()
        return 0, "创建成功", None

    def delete(self, user: UserDelete):
        statement = select(User).where(User.id == user.id)
        if user.name:
            statement = select(User).where(User.name == user.name)
        if not (db_user := self.db_session.exec(statement).first()):
            return -1, "用户不存在", None
        self.db_session.delete(db_user)
        self.db_session.commit()
        return 0, "删除成功", None

    def update(self, user: UserUpdate):
        db_user = self.db_session.get(User, user.id)
        if not db_user:
            return -1, "用户不存在", None
        db_user.name = user.name
        self.db_session.add(db_user)
        self.db_session.commit()
        return 0, "更新成功", None

    def select(self):
        statement = select(User).where(User.id == self.user_id)
        try:
            result = self.db_session.exec(statement).one()
        except NoResultFound:
            return "-1", "用户不存在", None
        else:
            return "0", "查询成功", result


router = APIRouter(prefix="/user", tags=["用户"])


@router.post("/create", response_model=ResponseBody, response_model_exclude_none=True)
async def create_user(user: UserCreate, request: Request, db_session: Session = Depends(get_session)):
    code, msg, result = UserService(request, db_session).create(user)
    return ResponseBody(code=code, msg=msg, data=result)


@router.post("/delete", response_model=ResponseBody, response_model_exclude_none=True)
async def delete_user(user: UserDelete, request: Request, db_session: Session = Depends(get_session)):
    code, msg, result = UserService(request, db_session).delete(user)
    return ResponseBody(code=code, msg=msg, data=result)


@router.post("/update", response_model=ResponseBody, response_model_exclude_none=True)
async def update_user(user: UserUpdate, request: Request, db_session: Session = Depends(get_session)):
    code, msg, result = UserService(request, db_session).update(user)
    return ResponseBody(code=code, msg=msg, data=result)


@router.post("/select", response_model=ResponseBody, response_model_exclude_none=True)
async def select_user(request: Request, db_session: Session = Depends(get_session)):
    """
    用户信息查询接口
    :param user:
    :param request:
    :param db_session:
    :return:
    """
    code, msg, result = UserService(request, db_session).select()
    return ResponseBody(code=code, msg=msg, data=result)
