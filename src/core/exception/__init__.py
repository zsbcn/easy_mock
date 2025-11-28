from core.constants import BaseEnum


class BusinessException(Exception):
    """
    业务异常
    """

    def __init__(self, error_info: BaseEnum):
        self.code = error_info.code
        self.message = error_info.message

    def as_dict(self):
        return {"code": self.code, "message": self.message}
