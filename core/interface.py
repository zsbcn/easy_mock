from typing import Any

from fastapi import APIRouter, Depends, Request
from loguru import logger
from sqlalchemy.exc import NoResultFound

from conf import get_session, Session, ResponseBody, select
from model.Interface import Interface, InterfaceCreate, InterfaceDelete, InterfaceUpdate, InterfaceSelect


class InterfaceConstants:
    INTERFACE_CREATE_SUCCESS = ("0", "接口创建成功")
    INTERFACE_UPDATE_SUCCESS = ("0", "接口更新成功")
    INTERFACE_DELETE_SUCCESS = ("0", "接口删除成功")
    INTERFACE_SELECT_SUCCESS = ("0", "接口查询成功")

    INTERFACE_URL_ERROR = ("-1", "接口URL格式错误, 建议的URL格式为'/user_id/xxx/xxx'")
    INTERFACE_DUPLICATION_ERROR = ("-2", "接口检查失败, 已存在Name, URL, Method相同的接口")
    INTERFACE_NOT_FOUND_ERROR = ("-3", "接口检查失败, 接口不存在或用户无权限")


class InterfaceService:
    """
    管理接口的服务类，包括接口的增删改查操作
    """

    def __init__(self, request: Request, db_session: Session):
        self.request = request
        self.db_session = db_session
        self.user_id = request.session.get("userId")

    def create(self, interface: InterfaceCreate) -> (str, str, Any):
        if not interface.url.startswith("/"):
            return *InterfaceConstants.INTERFACE_URL_ERROR, None
        # 检查待新增接口的URL是否已经在系统中存在，接口的URL全局唯一，不可重复
        statement = select(Interface).where(Interface.user_id == self.user_id, Interface.name == interface.name,
                                            Interface.url == interface.url,
                                            Interface.method == interface.method.upper())
        if self.db_session.exec(statement).fetchall():
            return *InterfaceConstants.INTERFACE_DUPLICATION_ERROR, None
        # 完成新增操作
        db_interface = Interface.model_validate(interface)
        # 补充user_id、处理method的值为大写
        db_interface.user_id = self.user_id
        db_interface.method = db_interface.method.upper()
        logger.info(db_interface)

        self.db_session.add(db_interface)
        self.db_session.commit()
        return *InterfaceConstants.INTERFACE_CREATE_SUCCESS, None

    def delete(self, interface: InterfaceDelete) -> (str, str, Any):
        # 检查待删除的接口是否存在，是否属于当前登录的用户
        statement = select(Interface).where(Interface.user_id == self.user_id, Interface.id == interface.id)
        try:
            result = self.db_session.exec(statement).one()
        except NoResultFound:
            return *InterfaceConstants.INTERFACE_NOT_FOUND_ERROR, None
        else:
            # 完成删除操作
            self.db_session.delete(result)
            self.db_session.commit()
            return *InterfaceConstants.INTERFACE_DELETE_SUCCESS, None

    def update(self, interface: InterfaceUpdate) -> (str, str, Any):
        # 检查待更新的接口是否存在，是否属于当前登录的用户
        statement = select(Interface).where(Interface.user_id == self.user_id)
        if not self.db_session.exec(statement.where(Interface.id == interface.id)).one():
            return *InterfaceConstants.INTERFACE_NOT_FOUND_ERROR, None
        # 检查新的URL是否全局唯一
        if self.db_session.exec(statement.where(Interface.id != interface.id, Interface.name == interface.name,
                                                Interface.url == interface.url,
                                                Interface.method == interface.method)).first():
            return *InterfaceConstants.INTERFACE_DUPLICATION_ERROR, None
        result = self.db_session.exec(statement.where(Interface.id == interface.id)).one()
        # 更新接口的字段值
        result.url = interface.url
        result.name = interface.name
        result.method = interface.method
        result.description = interface.description
        # 完成更新操作
        self.db_session.add(result)
        self.db_session.commit()
        return *InterfaceConstants.INTERFACE_UPDATE_SUCCESS, None

    def select(self, interface: InterfaceSelect) -> (str, str, Any):
        # 检查用户是否有权查看待查询的接口
        statement = select(Interface).where(Interface.user_id == self.user_id)
        if interface.id:
            statement = statement.where(getattr(Interface, "id").like(f"%{interface.id}%"))
        if interface.name:
            statement = statement.where(getattr(Interface, "name").like(f"%{interface.name}%"))
        if interface.url:
            statement = statement.where(getattr(Interface, "url").like(f"%{interface.url}%"))
        if interface.method:
            statement = statement.where(Interface.method == interface.method.upper())
        # 有权限则返回查询结果
        if not (result := self.db_session.exec(statement).fetchall()):
            return *InterfaceConstants.INTERFACE_NOT_FOUND_ERROR, None

        logger.info(result)
        # 删除查询结果中的user_id
        filter_result = []
        for item in result:
            item.user_id = None
            filter_result.append(item)
        return *InterfaceConstants.INTERFACE_SELECT_SUCCESS, filter_result


router = APIRouter(prefix="/interface", tags=["接口"])


@router.post('/create', response_model=ResponseBody, response_model_exclude_none=True)
async def create_interface(interface: InterfaceCreate, request: Request, db_session: Session = Depends(get_session)):
    logger.info(interface)
    code, msg, result = InterfaceService(request, db_session).create(interface)
    return ResponseBody(code=code, msg=msg, data=result)


@router.post('/delete', response_model=ResponseBody, response_model_exclude_none=True)
async def delete_interface(interface: InterfaceDelete, request: Request, db_session: Session = Depends(get_session)):
    logger.info(interface)
    code, msg, result = InterfaceService(request, db_session).delete(interface)
    return ResponseBody(code=code, msg=msg, data=result)


@router.post('/update', response_model=ResponseBody, response_model_exclude_none=True)
async def update_interface(interface: InterfaceUpdate, request: Request, db_session: Session = Depends(get_session)):
    logger.info(interface)
    code, msg, result = InterfaceService(request, db_session).update(interface)
    return ResponseBody(code=code, msg=msg, data=result)


@router.post('/select', response_model=ResponseBody, response_model_exclude_none=True)
async def select_interface(interface: InterfaceSelect, request: Request, db_session: Session = Depends(get_session)):
    logger.info(interface)
    code, msg, result = InterfaceService(request, db_session).select(interface)
    return ResponseBody(code=code, msg=msg, data=result)
