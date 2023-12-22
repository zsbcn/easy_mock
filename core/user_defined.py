import json

from fastapi import APIRouter, Depends, Request, Response

from conf import get_session, Session, select
from model.Interface import Interface
from model.Rule import Rule
from loguru import logger

router = APIRouter()


@router.api_route("/{interface_path:path}", methods=["GET", "POST"])
async def get_interface(interface_path: str, request: Request, session: Session = Depends(get_session)):
    interface_path = f"/{interface_path}"
    if request.method == "GET":
        input_content = request.query_params
    elif request.method == "POST":
        input_content = await request.json()
        input_content = json.dumps(input_content)
    else:
        input_content = ""
    logger.info(f"{interface_path},{request.method},{input_content}")
    statement = select(Rule).join(Interface, Interface.id == Rule.interface_id, isouter=True).where(
        Interface.url == interface_path, Interface.method == request.method, Rule.input_content == input_content)
    rule_info = session.exec(statement).one()
    logger.info(rule_info)
    return Response(content=rule_info.output_content, status_code=rule_info.status_code,
                    media_type=rule_info.response_media_type)
