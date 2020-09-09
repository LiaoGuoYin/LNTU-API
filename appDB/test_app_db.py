from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_connect_db():
    pass
