import json

from fastapi import APIRouter, Depends, Request, Response
from loguru import logger
from sqlalchemy.exc import NoResultFound

from conf import get_session, Session, select
from model.Interface import Interface
from model.Rule import Rule

router = APIRouter(tags=["自定义"], include_in_schema=False)


@router.api_route("{interface_path:path}", methods=["GET", "POST"])
async def get_interface(interface_path: str, request: Request, db_session: Session = Depends(get_session)):
    """
    用户自定义接口模拟桩的接口
    :param interface_path: 自定义模拟桩的URL
    :param request:
    :param db_session:
    :return: 满足规则的模拟桩结果
    """
    # 从请求中获取模拟桩的URL、method、请求参数、请求体等数据
    if request.method == "GET":
        input_content = request.query_params.__str__()
    elif request.method == "POST":
        input_content = await request.json()
        input_content = json.dumps(input_content)
    else:
        input_content = ""
    logger.info(f"{interface_path},{request.method},{input_content}")
    # 查询满足条件的模拟桩响应结果并返回
    statement = select(Rule).join(Interface, Interface.id == Rule.interface_id, isouter=True).where(
        Interface.url == interface_path, Interface.method == request.method, Rule.input_content == input_content)
    try:
        rule_info = db_session.exec(statement).one()
    except NoResultFound as e:
        return {"code": -1, "msg": f"{interface_path}接口未找到匹配的规则, 请在系统中新建接口和规划后使用"}
    else:
        logger.info(rule_info)
        return Response(content=rule_info.output_content, status_code=rule_info.status_code,
                        media_type=rule_info.response_media_type)
