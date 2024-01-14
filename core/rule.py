import json
from typing import Any

from fastapi import APIRouter, Request, Depends
from loguru import logger

from conf import get_session, Session, ResponseBody, select
from model.Interface import Interface
from model.Rule import Rule, RuleCreate, RuleDelete, RuleUpdate, RuleSelect


class RuleConstants:
    RULE_CREATE_SUCCESS = ("0", "接口规则新增成功")
    RULE_DELETE_SUCCESS = ("0", "接口规则删除成功")
    RULE_UPDATE_SUCCESS = ("0", "接口规则更新成功")
    RULE_SELECT_SUCCESS = ("0", "接口规则查询成功")

    RULE_NOT_FOUND_INTERFACE_ERROR = ("-1", "规则检查失败, 接口不存在或用户无权限")
    RULE_DUPLICATION_ERROR = ("-2", "规则检查失败, 接口已存在Input_Content相同的规则")
    RULE_NOT_EXIST_ERROR = ("-3", "规则检查失败, 规则不存在或用户无权限")


class RuleService:
    """
    接口规则的服务类
    """

    def __init__(self, request: Request, db_session: Session):
        self.request = request
        self.db_session = db_session
        self.user_id = request.session.get("userId")

    def get_base_statement(self, *, interface_id: int = None, rule_id: int = None, input_content: str = None,
                           output_content: str = None):
        statement = select(Rule).join(Interface, Interface.id == Rule.interface_id, isouter=True).where(
            Interface.user_id == self.user_id)
        if interface_id:
            statement = statement.where(Interface.id == interface_id)
        if rule_id:
            statement = statement.where(Rule.id == rule_id)
        if input_content:
            statement = statement.where(Rule.input_content == input_content)
        if output_content:
            statement = statement.where(Rule.output_content == output_content)
        return statement

    def check_rule(self, *, interface_id: int = None, rule_id: int = None):
        pass

    def create(self, rule: RuleCreate) -> (str, str, Any):
        # 检查待新增的规则是否与已有的冲突
        statement = select(Rule).where(Rule.interface_id == rule.interface_id, Rule.input_content == rule.input_content)
        if self.db_session.exec(statement).fetchall():
            return *RuleConstants.RULE_DUPLICATION_ERROR, None
        if rule.request_media_type.lower() == "application/json":
             rule.input_content = json.dumps(json.loads(rule.input_content))

        if rule.response_media_type.lower() == "application/json":
            rule.output_content = json.dumps(json.loads(rule.output_content))

        # 完成新增操作
        db_rule = Rule.model_validate(rule)
        self.db_session.add(db_rule)
        self.db_session.commit()
        return *RuleConstants.RULE_CREATE_SUCCESS, None

    def delete(self, rule: RuleDelete) -> (str, str, Any):
        # 检查待删除的规则是否存在
        if not self.db_session.exec(select(Rule).where(Rule.id == rule.id)).fetchall():
            return *RuleConstants.RULE_NOT_EXIST_ERROR, None

        # 完成删除操作
        result = self.db_session.get(Rule, rule.id)
        self.db_session.delete(result)
        self.db_session.commit()
        return *RuleConstants.RULE_DELETE_SUCCESS, None

    def update(self, rule: RuleUpdate) -> (str, str, Any):
        # 检查用户是否有待更新的规则所属接口的权限
        if not self.db_session.exec(select(Rule).where(Rule.id == rule.id)).fetchall():
            return *RuleConstants.RULE_NOT_EXIST_ERROR, None

        # 检查待更新的规则是否与已有规则重复
        if self.db_session.exec(self.get_base_statement(interface_id=rule.interface_id, rule_id=rule.id).where(
                Rule.input_content != rule.input_content, Rule.output_content != rule.output_content)).fetchall():
            return *RuleConstants.RULE_DUPLICATION_ERROR, None
        # 更新规则字段
        result = self.db_session.get(Rule, rule.id)
        result.input_content = rule.input_content
        result.output_content = rule.output_content
        result.result_content_type = rule.result_content_type
        result.status_code = rule.status_code
        # 完成更新操作
        self.db_session.add(result)
        self.db_session.commit()
        return *RuleConstants.RULE_UPDATE_SUCCESS, None

    def select(self, rule: RuleSelect) -> (str, str, Any):
        # # 检查用户下的接口及规则是否存在
        if rule.interface_id:
            statement = select(Interface).where(getattr(Interface, "id").like(f"%{rule.interface_id}%"))
            if not self.db_session.exec(statement).fetchall():
                return *RuleConstants.RULE_NOT_FOUND_INTERFACE_ERROR, None
        statement = (select(Rule))
        if rule.interface_id:
            statement = statement.where(getattr(Rule, "interface_id").like(f"%{rule.interface_id}%"))
        if rule.id:
            statement = statement.where(getattr(Rule, "id").like(f"%{rule.id}%"))
        if rule.input_content:
            statement = statement.where(getattr(Rule, "input_content").like(f"%{rule.input_content}%"))
        if rule.output_content:
            statement = statement.where(getattr(Rule, "output_content").like(f"%{rule.output_content}%"))

        # 返回用户所有有权限的接口的规则
        if not (result := self.db_session.exec(statement).fetchall()):
            logger.info(statement)
            logger.info(f"响应内容: {result}")
            return *RuleConstants.RULE_SELECT_SUCCESS, []
        return *RuleConstants.RULE_SELECT_SUCCESS, result


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
