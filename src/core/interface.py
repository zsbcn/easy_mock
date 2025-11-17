from typing import Any

from fastapi import APIRouter, Depends, Request
from loguru import logger

from src.conf import get_session, Session, ResponseBody, select, SUPPORT_METHODS
from src.model.Interface import Interface, InterfaceCreate, InterfaceDelete, InterfaceUpdate, InterfaceSelect, \
    InterfaceStatus, InterfaceResponse
from src.model.Rule import Rule


class InterfaceConstants:
    INTERFACE_CREATE_SUCCESS = ("0", "接口创建成功")
    INTERFACE_UPDATE_SUCCESS = ("0", "接口更新成功")
    INTERFACE_DELETE_SUCCESS = ("0", "接口删除成功")
    INTERFACE_SELECT_SUCCESS = ("0", "接口查询成功")
    INTERFACE_CHANGE_STATUS_SUCCESS = ("0", "接口状态修改成功")

    INTERFACE_URL_ERROR = ("-1", "接口URL格式错误, 建议的URL格式为'/user_id/xxx/xxx'")
    INTERFACE_METHOD_ERROR = ("-2", f"接口Method格式错误, 建议的Method格式为{','.join(SUPPORT_METHODS)}")
    INTERFACE_DUPLICATION_ERROR = ("-3", "接口检查失败, 已存在Name, URL, Method相同的接口")
    INTERFACE_NOT_FOUND_ERROR = ("-4", "接口检查失败, 接口不存在或用户无权限")
    INTERFACE_DELETE_HAVE_ERROR = ("-5", "接口删除失败, 接口可能不存在或用户无权限或者接口下仍关联有规则")


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
        if interface.method.upper() not in SUPPORT_METHODS:
            return *InterfaceConstants.INTERFACE_METHOD_ERROR, None
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

    def delete(self, interfaces: InterfaceDelete) -> (str, str, Any):
        delete_result = []
        for interface_id in interfaces.id:
            # 检查待删除的接口是否存在，是否属于当前登录的用户
            statement = select(Interface).where(Interface.user_id == self.user_id, Interface.id == interface_id)
            interface_info = self.db_session.exec(statement).first()
            statement = select(Rule).where(Rule.interface_id == interface_id)
            rules = self.db_session.exec(statement).all()
            logger.info(interface_info)
            logger.info(rules)
            if interface_info and rules:
                delete_result.append({"id": interface_id, "error": "接口下存在关联规则，无法删除"})
            elif interface_info:
                # 完成删除操作
                self.db_session.delete(interface_info)
                self.db_session.commit()
            else:
                delete_result.append({"id": interface_id, "error": "接口不存在或用户无权限"})
        if delete_result:
            return *InterfaceConstants.INTERFACE_DELETE_HAVE_ERROR, delete_result
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
            return *InterfaceConstants.INTERFACE_SELECT_SUCCESS, []
        logger.info(result)
        # 删除查询结果中的user_id
        filter_result = []
        for item in result:
            item.user_id = None
            filter_result.append(item)
        return *InterfaceConstants.INTERFACE_SELECT_SUCCESS, filter_result

    def change_status(self, interface: InterfaceStatus) -> (str, str, Any):
        # 检查待更新的接口是否存在，是否属于当前登录的用户
        statement = select(Interface).where(Interface.user_id == self.user_id)
        if not self.db_session.exec(statement.where(Interface.id == interface.id)).one():
            return *InterfaceConstants.INTERFACE_NOT_FOUND_ERROR, None
        result = self.db_session.get(Interface, interface.id)
        result.status = bool(interface.status)
        self.db_session.commit()
        return *InterfaceConstants.INTERFACE_CHANGE_STATUS_SUCCESS, None

    def select2(self, interface: InterfaceSelect) -> (str, str, Any):
        statement = select(Interface).where(Interface.user_id == self.user_id, Interface.id == interface.id)
        result = self.db_session.exec(statement).fetchall()
        logger.info(result)
        temp = []
        for item in result:
            temp.append(
                InterfaceResponse(id=item.id, name=item.name, url=item.url, method=item.method,
                                  description=item.description, status=item.status, rules=item.rules))
        return *InterfaceConstants.INTERFACE_CHANGE_STATUS_SUCCESS, temp


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


@router.post('/change_status', response_model=ResponseBody, response_model_exclude_none=True)
async def change_status(interface: InterfaceStatus, request: Request, db_session: Session = Depends(get_session)):
    logger.info(interface)
    code, msg, result = InterfaceService(request, db_session).change_status(interface)
    return ResponseBody(code=code, msg=msg, data=result)


@router.post('/select2', response_model=ResponseBody, response_model_exclude_none=True)
async def select_interface(interface: InterfaceSelect, request: Request, db_session: Session = Depends(get_session)):
    logger.info(interface)
    code, msg, result = InterfaceService(request, db_session).select2(interface)
    return ResponseBody(code=code, msg=msg, data=result)
