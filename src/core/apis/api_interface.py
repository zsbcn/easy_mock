from fastapi import APIRouter, Depends

from conf import ResponseBody
from core.depends import get_interface_service, get_user_id, get_project_service
from core.models.model_interface import InterfaceCreate
from core.services.service_interface import InterfaceService
from core.services.service_project import ProjectService

router = APIRouter(tags=["接口"])


@router.get("/interface_list")
async def interface_list(project_id: str,
                         project_service: ProjectService = Depends(get_project_service),
                         interface_service: InterfaceService = Depends(get_interface_service),
                         user_id: str = Depends(get_user_id)):
    """
    获取接口列表
    :param project_id:
    :param project_service:
    :param interface_service:
    :param user_id:
    :return:
    """
    project_service.check_project_by_user_id(user_id, project_id)
    return ResponseBody(data=interface_service.get_interface_list(project_id))


@router.post("/create_interface")
async def create_interface(interface_create: InterfaceCreate,
                           project_service: ProjectService = Depends(get_project_service),
                           interface_service: InterfaceService = Depends(get_interface_service),
                           user_id: str = Depends(get_user_id)):
    """
    创建接口
    :param interface_create:
    :param project_service:
    :param interface_service:
    :param user_id:
    :return:
    """
    project_service.check_project_by_user_id(user_id, interface_create.project_id)
    interface_service.create_interface(interface_create, user_id)
