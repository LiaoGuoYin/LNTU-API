from starlette.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"Hi": "LNTU-API-v1.0"}
