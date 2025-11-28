from core.constants import LoginConstants
from core.exception import BusinessException
from core.models.model_user import UserLogin, User
from core.services import BaseService


class LoginService(BaseService):
    def login(self, user: UserLogin):
        user_exist = self.db.query(User).where(User.username == user.username, User.password == user.password).first()
        if not user_exist:
            raise BusinessException(LoginConstants.FAILED)
