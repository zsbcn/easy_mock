from fastapi import APIRouter, Request, Depends
from fastapi.logger import logger

from conf import get_session, Session, ResponseBody, select
from model.Interface import Interface
from model.Rule import Rule, RuleCreate, RuleDelete, RuleUpdate, RuleSelect


class RuleService:
    """
    接口规则的服务类
    """

    def __init__(self, request: Request, db_session: Session):
        self.request = request
        self.db_session = db_session
        self.user_id = request.session.get("userId")

    @staticmethod
    def get_base_statement():
        return select(Rule).join(Interface, Interface.id == Rule.interface_id, isouter=True)

    def create(self, rule: RuleCreate):
        # 检查用户是否有待增加规则的接口的权限
        statement = select(Interface).where(Interface.user_id == self.user_id, Interface.id == rule.interface_id)
        if not self.db_session.exec(statement).fetchall():
            return -1, "接口不存在或用户无接口权限", None
        # 检查待新增的规则是否与已有的冲突
        statement = RuleService.get_base_statement().where(Interface.user_id == self.user_id,
                                                           Interface.id == rule.interface_id)
        if self.db_session.exec(statement.where(Rule.input_content == rule.input_content)).fetchall():
            return -1, "接口输入规则冲突", None
        # 完成新增操作
        db_rule = Rule.model_validate(rule)
        self.db_session.add(db_rule)
        self.db_session.commit()
        return 0, "接口规则新增成功", None

    def delete(self, rule: RuleDelete):
        # 检查用户是否有待删除规则所属接口的权限
        statement = RuleService.get_base_statement().where(Interface.user_id == self.user_id,
                                                           Interface.id == rule.interface_id)
        if not self.db_session.exec(statement).fetchall():
            return -1, "接口不存在或用户无接口权限", None
        # 检查待删除的规则是否存在
        if not self.db_session.exec(statement.where(Rule.id == rule.id)).fetchall():
            return -1, "接口规则不存在", None
        # 完成删除操作
        result = self.db_session.get(Rule, rule.id)
        self.db_session.delete(result)
        self.db_session.commit()
        return 0, "接口规则删除成功", None

    def update(self, rule: RuleUpdate):
        # 检查用户是否有待更新的规则所属接口的权限
        statement = RuleService.get_base_statement().where(Interface.user_id == self.user_id,
                                                           Interface.id == rule.interface_id)
        if not self.db_session.exec(statement.where(Rule.id == rule.id)).fetchall():
            return -1, "接口规则不存在、或接口不存在、或用户无接口权限", None
        # 检查待更新的规则是否与已有规则重复
        if self.db_session.exec(statement.where(Rule.input_content != rule.input_content)).fetchall():
            return -1, "接口规则更新失败, 接口规则冲突", None
        # 更新规则字段
        result = self.db_session.get(Rule, rule.id)
        result.input_content = rule.input_content
        result.output_content = rule.output_content
        result.result_content_type = rule.result_content_type
        result.status_code = rule.status_code
        # 完成更新操作
        self.db_session.add(result)
        self.db_session.commit()
        return 0, "接口规则更新成功", None

    def select(self, rule: RuleSelect):
        # 检查用户下的接口及规则是否存在
        statement = RuleService.get_base_statement().where(Interface.user_id == self.user_id)
        if rule.id:
            statement = statement.where(Rule.id == rule.id)
        if rule.interface_id:
            statement = statement.where(Rule.interface_id == rule.interface_id)
        # 返回用户所有有权限的接口的规则
        if not (result := self.db_session.exec(statement).fetchall()):
            return -1, "接口规则为空、或接口不存在、或用户无接口权限", None
        return 0, "接口查询成功", result


router = APIRouter(prefix="/rule", tags=["规则"])


@router.post("/create", response_model=ResponseBody, response_model_exclude_none=True)
async def create_rule(rule: RuleCreate, request: Request, db_session: Session = Depends(get_session)):
    logger.info(rule)
    code, msg, result = RuleService(request, db_session).create(rule)
    return ResponseBody(code=code, msg=msg, data=result)


@router.post("/delete", response_model=ResponseBody, response_model_exclude_none=True)
async def delete_rule(rule: RuleDelete, request: Request, db_session: Session = Depends(get_session)):
    code, msg, result = RuleService(request, db_session).delete(rule)
    return ResponseBody(code=code, msg=msg, data=result)


@router.post("/update", response_model=ResponseBody, response_model_exclude_none=True)
async def update_rule(rule: RuleUpdate, request: Request, db_session: Session = Depends(get_session)):
    code, msg, result = RuleService(request, db_session).update(rule)
    return ResponseBody(code=code, msg=msg, data=result)


@router.post("/select", response_model=ResponseBody, response_model_exclude_none=True)
async def select_rule(rule: RuleSelect, request: Request, db_session: Session = Depends(get_session)):
    code, msg, result = RuleService(request, db_session).select(rule)
    return ResponseBody(code=code, msg=msg, data=result)
