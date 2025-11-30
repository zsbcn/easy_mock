from core.constants import UserConstants
from core.exception import BusinessException
from core.models.model_project import Project, ProjectSelect
from core.models.model_user import UserResponse, User, UserInfo
from core.models.model_user_project import UserProject
from core.services import BaseService


class UserService(BaseService):
    def user_list(self) -> list[UserResponse]:
        """
        获取用户列表
        :return:
        """
        result = self.db.query(User).all()
        return [UserResponse.model_validate(user) for user in result]

    def get_user_info(self, user_id: str):
        """
        获取用户信息
        :param user_id:
        :return:
        """
        user = self.db.query(User).where(User.user_id == user_id).first()
        if not user:
            raise BusinessException(UserConstants.NO_EXIST)
        project_id_list: list[UserProject] = self.db.query(UserProject).where(UserProject.user_id == user_id).all()
        project_list: list[Project] = self.db.query(Project).where(
            Project.id.in_([project.project_id for project in project_id_list])).all()
        return UserInfo(user_id=user.user_id, username=user.username, status=user.status,
                        project_list=[ProjectSelect.model_validate(project) for project in project_list])
