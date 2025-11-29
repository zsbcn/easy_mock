from core.models.model_user import UserResponse, User
from core.services import BaseService



class UserService(BaseService):
    def user_list(self) -> list[UserResponse]:
        """
        获取用户列表
        :return:
        """
        result = self.db.query(User).all()
        return [UserResponse.model_validate(user) for user in result]
