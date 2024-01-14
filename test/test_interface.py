import pytest
from fastapi.testclient import TestClient

from core.interface import InterfaceConstants
from core.login import LoginConstants
from main import app

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def login():
    response = client.post("/login", json={"id": "zwx1199119", "name": "zhangshibin"})
    assert response.status_code == 200
    code, msg = LoginConstants.USER_LOGIN_SUCCESS
    assert response.json() == {"code": code, "msg": msg}
    yield
    print("后置处理")


def check_interface_exist(interface: dict):
    response = client.post("/interface/select", json=interface)
    assert response.status_code == 200
    code, msg = InterfaceConstants.INTERFACE_NOT_FOUND_ERROR
    assert response.json() == {"code": code, "msg": msg}


def delete_interface(interface: dict):
    response = client.post("/interface/select", json=interface)
    assert response.status_code == 200
    interface_id = response.json()["data"][0]["id"]
    response = client.post("/interface/delete", json={"id": interface_id})
    assert response.status_code == 200
    code, msg = InterfaceConstants.INTERFACE_DELETE_SUCCESS
    assert response.json() == {"code": code, "msg": msg}


def test_interface_create_success():
    newInterface = {"name": "test", "url": "/test", "method": "GET", "description": "test"}
    # 环境检查
    check_interface_exist(newInterface)

    # 测试步骤
    response = client.post("/interface/create", json=newInterface)
    assert response.status_code == 200
    code, msg = InterfaceConstants.INTERFACE_CREATE_SUCCESS
    assert response.json() == {"code": code, "msg": msg}

    # 数据清理
    delete_interface(newInterface)


def test_interface_create_fail_url_error():
    newInterface = {"name": "test", "url": "test", "method": "GET", "description": "test"}
    # 环境检查
    check_interface_exist(newInterface)

    # 测试步骤
    response = client.post("/interface/create", json=newInterface)
    assert response.status_code == 200
    code, msg = InterfaceConstants.INTERFACE_URL_ERROR
    assert response.json() == {"code": code, "msg": msg}

    # 数据清理
    pass


def test_interface_create_fail_method_error():
    newInterface = {"name": "test", "url": "/test", "method": "test", "description": "test"}
    # 环境检查
    check_interface_exist(newInterface)

    # 测试步骤
    response = client.post("/interface/create", json=newInterface)
    assert response.status_code == 200
    code, msg = InterfaceConstants.INTERFACE_METHOD_ERROR
    assert response.json() == {"code": code, "msg": msg}

    # 数据清理
    pass


def test_interface_create_fail_duplicate_error():
    newInterface = {"name": "test", "url": "/test", "method": "GET", "description": "test"}
    # 环境检查
    check_interface_exist(newInterface)
    client.post("/interface/create", json=newInterface)

    # 测试步骤
    response = client.post("/interface/create", json=newInterface)
    assert response.status_code == 200
    code, msg = InterfaceConstants.INTERFACE_DUPLICATION_ERROR
    assert response.json() == {"code": code, "msg": msg}

    # 数据清理
    delete_interface(newInterface)


def test_interface_delete_success():
    newInterface = {"name": "test", "url": "/test", "method": "GET", "description": "test"}
    # 环境检查
    check_interface_exist(newInterface)
    client.post("/interface/create", json=newInterface)

    # 测试步骤
    response = client.post("/interface/select", json=newInterface)
    assert response.status_code == 200
    interface_id = response.json()["data"][0]["id"]
    response = client.post("/interface/delete", json={"id": interface_id})
    assert response.status_code == 200
    code, msg = InterfaceConstants.INTERFACE_DELETE_SUCCESS
    assert response.json() == {"code": code, "msg": msg}

    # 数据清理
    pass


def test_interface_delete_fail_not_exist_error():
    interface = {"id": "1"}
    # 环境检查
    check_interface_exist(interface)

    # 测试步骤
    response = client.post("/interface/delete", json=interface)
    assert response.status_code == 200
    code, msg = InterfaceConstants.INTERFACE_NOT_FOUND_ERROR
    assert response.json() == {"code": code, "msg": msg}

    # 数据清理
    pass


if __name__ == '__main__':
    pytest.main(["-ss", "./test/test_interface.py"])
