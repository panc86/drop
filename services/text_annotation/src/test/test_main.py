import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    yield TestClient(app)


def test_ping(client):
    response = client.get("/ping/")
    assert response.status_code == 200 and response.json() == "pong"
