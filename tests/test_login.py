from fastapi.testclient import TestClient

from src.conf import LoginConstants
from src.main import app

client = TestClient(app)


def test_login_success():
    response = client.post("/login", json={"id": "zwx1199119", "name": "zhangshibin"})
    assert response.status_code == 200
    code, msg = LoginConstants.USER_LOGIN_SUCCESS
    assert response.json() == {"code": code, "msg": msg}


def test_login_failed_user_not_exist():
    response = client.post("/login", json={"id": "admin", "name": "admin"})
    assert response.status_code == 200
    code, msg = LoginConstants.USER_NOT_EXIST
    assert response.json() == {"code": code, "msg": msg}


def test_login_failed_user_info_error():
    response = client.post("/login", json={"id": "zwx1199119", "name": "admin"})
    assert response.status_code == 200
    code, msg = LoginConstants.USER_LOGIN_FAILED
    assert response.json() == {"code": code, "msg": msg}
