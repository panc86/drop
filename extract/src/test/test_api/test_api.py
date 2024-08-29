import pytest
from fastapi.testclient import TestClient

from extract.api import router


@pytest.fixture
def client():
    yield TestClient(router.app)


def test_ping(client):
    response = client.get("/ping/")
    assert response.status_code == 200 and response.json() == "pong"
