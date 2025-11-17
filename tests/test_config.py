import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_config_with_group():
    response = client.get("/config/methods")
    assert response.status_code == 200
    print(response.json())


if __name__ == '__main__':
    pytest.main(["-ss", "./test/test_config.py"])
