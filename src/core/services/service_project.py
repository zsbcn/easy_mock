from loguru import logger
from sqlalchemy.exc import IntegrityError

from core.constants import ProjectConstants
from core.exception import BusinessException
from core.models.model_project import Project, ProjectCreate, ProjectResponse
from core.models.model_user_project import UserProject
from core.services import BaseService


class ProjectService(BaseService):
    def get_project_list(self) -> list[ProjectResponse]:
        project_list: list[Project] = self.db.query(Project).all()
        return [ProjectResponse.model_validate(project) for project in project_list]

    def create_project(self, project: ProjectCreate, user_id: str) -> None:
        project_exist: Project = self.db.query(Project).where(Project.name == project.name).first()
        if project_exist:
            raise BusinessException(ProjectConstants.PROJECT_EXIST)
        project = Project(create_by=user_id, **project.model_dump())
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        try:
            self.db.add(UserProject(user_id=user_id, project_id=project.id))
        except IntegrityError:
            logger.warning("用户项目关系数据已存在.")
        else:
            self.db.commit()
