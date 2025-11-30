from core.constants import RegisterConstants
from core.exception import BusinessException
from core.models.model_user import User, UserCreate
from core.services import BaseService
from core.utils import hash_password


class RegisterService(BaseService):
    def register(self, user: UserCreate):
        user_exist = self.db.query(User).where(User.user_id == user.user_id).first()
        if user_exist:
            raise BusinessException(RegisterConstants.USER_EXIST)
        hashed_password, salt = hash_password(user.password)
        new_user = User(password=hashed_password, salt=salt, **user.model_dump(exclude=("password",)))
        self.db.add(new_user)
        self.db.commit()
