from fastapi import APIRouter, Request, Depends
from fastapi.logger import logger

from conf import get_session, Session, Response, select
from model.Interface import Interface
from model.Rule import Rule, RuleCreate, RuleDelete, RuleUpdate, RuleSelect


class RuleService:
    def __init__(self, request: Request, session: Session):
        self.request = request
        self.session = session
        self.user_id = request.session.get("user_id")

    @staticmethod
    def get_base_statement():
        return select(Rule).join(Interface, Interface.id == Rule.interface_id, isouter=True)

    def create(self, rule: RuleCreate):
        statement = select(Interface).where(Interface.user_id == self.user_id, Interface.id == rule.interface_id)
        if not self.session.exec(statement).fetchall():
            return -1, "接口不存在或用户无接口权限", None
        statement = RuleService.get_base_statement().where(Interface.user_id == self.user_id,
                                                           Interface.id == rule.interface_id)
        if self.session.exec(statement.where(Rule.input_content == rule.input_content)).fetchall():
            return -1, "接口输入规则冲突", None
        db_rule = Rule.model_validate(rule)
        # db_rule.method = db_rule.method.upper()
        self.session.add(db_rule)
        self.session.commit()
        return 0, "接口规则新增成功", None

    def delete(self, rule: RuleDelete):
        statement = RuleService.get_base_statement().where(Interface.user_id == self.user_id,
                                                           Interface.id == rule.interface_id)
        if not self.session.exec(statement).fetchall():
            return -1, "接口不存在或用户无接口权限", None
        if not self.session.exec(statement.where(Rule.id == rule.id)).fetchall():
            return -1, "接口规则不存在", None
        result = self.session.get(Rule, rule.id)
        self.session.delete(result)
        self.session.commit()
        return 0, "接口规则删除成功", None

    def update(self, rule: RuleUpdate):
        statement = RuleService.get_base_statement().where(Interface.user_id == self.user_id,
                                                           Interface.id == rule.interface_id)
        if not self.session.exec(statement.where(Rule.id == rule.id)).fetchall():
            return -1, "接口规则不存在、或接口不存在、或用户无接口权限", None
        if self.session.exec(statement.where(Rule.input_content != rule.input_content)).fetchall():
            return -1, "接口规则更新失败, 接口规则冲突", None
        result = self.session.get(Rule, rule.id)
        # result.method = result.method.upper()
        result.input_content = rule.input_content
        result.output_content = rule.output_content
        result.result_content_type = rule.result_content_type
        result.status_code = rule.status_code
        self.session.add(result)
        self.session.commit()
        return 0, "接口规则更新成功", None

    def select(self, rule: RuleSelect):
        statement = RuleService.get_base_statement().where(Interface.user_id == self.user_id)
        if rule.id:
            statement = statement.where(Rule.id == rule.id)
        if rule.interface_id:
            statement = statement.where(Rule.interface_id == rule.interface_id)
        if not (result := self.session.exec(statement).fetchall()):
            return -1, "接口规则为空、或接口不存在、或用户无接口权限", None
        return 0, "接口查询成功", result


router = APIRouter(prefix="/rule")


@router.post("/create", response_model=Response, response_model_exclude_none=True)
async def create_rule(rule: RuleCreate, request: Request, session: Session = Depends(get_session)):
    logger.info(rule)
    code, msg, result = RuleService(request, session).create(rule)
    return Response(code=code, msg=msg, data=result)


@router.post("/delete", response_model=Response, response_model_exclude_none=True)
async def delete_rule(rule: RuleDelete, request: Request, session: Session = Depends(get_session)):
    code, msg, result = RuleService(request, session).delete(rule)
    return Response(code=code, msg=msg, data=result)


@router.post("/update", response_model=Response, response_model_exclude_none=True)
async def update_rule(rule: RuleUpdate, request: Request, session: Session = Depends(get_session)):
    code, msg, result = RuleService(request, session).update(rule)
    return Response(code=code, msg=msg, data=result)


@router.post("/select", response_model=Response, response_model_exclude_none=True)
async def select_rule(rule: RuleSelect, request: Request, session: Session = Depends(get_session)):
    code, msg, result = RuleService(request, session).select(rule)
    return Response(code=code, msg=msg, data=result)
