class LoginConstants:
    USER_LOGOUT_SUCCESS = ("0", "用户登出成功")
    USER_LOGIN_SUCCESS = ("0", "用户登录成功")
    USER_LOGIN_FAILED = ("1001", "用户登录失败")
    USER_NOT_LOGIN = ("1002", "用户未登录")
    USER_NOT_EXIST = ("1003", "用户不存在")
    USER_PASSWORD_ERROR = ("1004", "用户密码错误")


class InterfaceConstants:
    INTERFACE_CREATE_SUCCESS = ("0", "接口创建成功")
    INTERFACE_UPDATE_SUCCESS = ("0", "接口更新成功")
    INTERFACE_DELETE_SUCCESS = ("0", "接口删除成功")


if __name__ == '__main__':
    print(LoginConstants.USER_LOGIN_FAILED)
