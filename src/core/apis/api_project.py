from fastapi import APIRouter, Depends, Request

from conf import ResponseBody
from core.depends import get_project_service, get_redis_service
from core.models.model_project import ProjectCreate
from core.services.service_project import ProjectService
from core.services.service_redis import RedisService

router = APIRouter(tags=["项目"])


@router.get("/project_list")
async def project_list(project_service: ProjectService = Depends(get_project_service)):
    """
    项目列表
    """
    return ResponseBody(data=project_service.get_project_list())


@router.post("/project_create")
async def project_create(request: Request, project: ProjectCreate,
                         project_service: ProjectService = Depends(get_project_service),
                         redis_service: RedisService = Depends(get_redis_service)):
    """
    项目创建
    """
    session_id = request.session.get("sessionId")
    user_id = await redis_service.get_str(f"session:{session_id}")
    return ResponseBody(data=project_service.create_project(project, user_id))
