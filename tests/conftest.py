import pytest
from fastapi.testclient import TestClient
from crud_analytics_api.app import app



@pytest.fixture
def client():
    return TestClient(app)

    