from core.constants import RegisterConstants
from core.exception import BusinessException
from core.models.model_user import User, UserCreate
from core.services import BaseService


class RegisterService(BaseService):
    def register(self, user: UserCreate):
        user_exist = self.db.query(User).where(User.username == user.username).first()
        if user_exist:
            raise BusinessException(RegisterConstants.USER_EXIST)
        new_user = User(username=user.username, password=user.password)
        self.db.add(new_user)
        self.db.commit()
