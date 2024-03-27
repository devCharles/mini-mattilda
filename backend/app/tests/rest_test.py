from fastapi.testclient import TestClient
from app.models import SchoolCreate, SchoolUpdate
from unittest.mock import Mock
from app.db.db import get_db_session

from app.rest.main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json().get("message") is not None


def test_create_new_school():
    session = Mock()
    cache = Mock()
    school = SchoolCreate(sid="TESTSCHOOL01", name="Test School", address="123 Test St")
    response = client.post("/schools/", json=school.model_dump())
    assert response.status_code == 200
