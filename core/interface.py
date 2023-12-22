from fastapi import APIRouter, Depends, Request

from conf import get_session, Session, Response, select
from model.Interface import Interface, InterfaceCreate, InterfaceDelete, InterfaceUpdate, InterfaceSelect


class InterfaceService:
    """
    管理接口的服务类，包括接口的增删改查操作
    """

    def __init__(self, request: Request, session: Session):
        self.request = request
        self.session = session
        self.user_id = request.session.get("user_id")

    def create(self, interface: InterfaceCreate):
        # 检查待新增接口的URL是否已经在系统中存在，接口的URL全局唯一，不可重复
        statement = select(Interface).where(Interface.url == interface.url)
        if self.session.exec(statement).fetchall():
            return -1, "接口新增失败, 已存在重复URL的接口, 建议的URL格式为'/user_id/xxx/xxx'", None
        # 补充user_id、处理method的值为大写
        interface.user_id = self.user_id
        interface.method = interface.method.upper()
        # 完成新增操作
        db_interface = Interface.model_validate(interface)
        self.session.add(db_interface)
        self.session.commit()
        return 0, "接口新增成功", None

    def delete(self, interface: InterfaceDelete):
        # 检查待删除的接口是否存在，是否属于当前登录的用户
        statement = select(Interface).where(Interface.user_id == self.user_id, Interface.id == interface.id)
        if not (result := self.session.exec(statement).fetchall()):
            return -1, "接口不存在或用户无权限", None
        # 完成删除操作
        self.session.delete(result)
        self.session.commit()
        return 0, "接口删除成功", None

    def update(self, interface: InterfaceUpdate):
        # 检查待更新的接口是否存在，是否属于当前登录的用户
        statement = select(Interface).where(Interface.user_id == self.user_id, Interface.id == interface.id)
        if not (result := self.session.exec(statement).fetchall()):
            return -1, "接口不存在或用户无权限", None
        # 检查新的URL是否全局唯一
        if self.session.exec(statement.where(Interface.url == interface.url)):
            return -1, "接口更新失败, 接口URL冲突", None

        # 更新接口的字段值
        result.url = interface.url
        result.name = interface.name
        result.method = interface.method
        result.description = interface.description
        # 完成更新操作
        self.session.add(result)
        self.session.commit()
        return 0, "接口更新成功", None

    def select(self, interface: InterfaceSelect):
        # 检查用户是否有权查看待查询的接口
        statement = select(Interface).where(Interface.user_id == self.user_id)
        if interface.id:
            statement = statement.where(Interface.id == interface.id)
        # 有权限则返回查询结果
        if not (result := self.session.exec(statement).fetchall()):
            return -1, "接口不存在或用户无权限", None
        return 0, "接口查询成功", result


router = APIRouter(prefix="/interface", tags=["接口"])


@router.post('/create', response_model=Response, response_model_exclude_none=True)
async def create_interface(interface: InterfaceCreate, request: Request, session: Session = Depends(get_session)):
    code, msg, result = InterfaceService(request, session).create(interface)
    return Response(code=code, msg=msg, data=result)


@router.post('/delete', response_model=Response, response_model_exclude_none=True)
async def delete_interface(interface: InterfaceDelete, request: Request, session: Session = Depends(get_session)):
    code, msg, result = InterfaceService(request, session).delete(interface)
    return Response(code=code, msg=msg, data=result)


@router.post('/update', response_model=Response, response_model_exclude_none=True)
async def update_interface(interface: InterfaceUpdate, request: Request, session: Session = Depends(get_session)):
    code, msg, result = InterfaceService(request, session).update(interface)
    return Response(code=code, msg=msg, data=result)


@router.post('/select', response_model=Response, response_model_exclude_none=True)
async def select_interface(interface: InterfaceSelect, request: Request, session: Session = Depends(get_session)):
    code, msg, result = InterfaceService(request, session).select(interface)
    return Response(code=code, msg=msg, data=result)
