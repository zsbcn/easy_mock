from core.constants import LoginConstants
from core.exception import BusinessException
from core.models.model_user import UserLogin, User
from core.services import BaseService
from core.utils import check_password


class LoginService(BaseService):
    def login(self, user: UserLogin):
        user_exist: User = self.db.query(User).where(User.user_id == user.user_id).first()
        if not user_exist:
            raise BusinessException(LoginConstants.FAILED)
        if not check_password(user.password, user_exist.salt, user_exist.password):
            raise BusinessException(LoginConstants.FAILED)
