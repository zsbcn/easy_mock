from enum import Enum


class BaseEnum(Enum):
    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message

    def as_dict(self):
        return {"code": self.code, "message": self.message}


class RegisterConstants(BaseEnum):
    SUCCESS = ("0", "用户注册成功")
    USER_EXIST = ("1001", "用户已存在")


class LoginConstants(BaseEnum):
    SUCCESS = ("0", "登录成功")
    FAILED = ("2001", "用户账号或密码错误")
    NOT_LOGIN = ("2002", "用户未登录")


class LogoutConstants(BaseEnum):
    SUCCESS = ("0", "退出登录成功")
    FAILED = ("3001", "退出登录失败")


class UserConstants(BaseEnum):
    SUCCESS = ("0", "成功")
    NO_EXIST = ("2001", "用户不存在")


class ProjectConstants(BaseEnum):
    SUCCESS = ("0", "项目创建成功")
    PROJECT_EXIST = ("3001", "项目已存在")
