import pytest

from redis import Redis
from sqlmodel.pool import StaticPool
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from fastapi.testclient import TestClient

from app.rest.main import app
from app.db.cache import get_redis_client
from app.models import SchoolCreate

from app.db.db import get_db_session

client = TestClient(app)


## shared fixtures


@pytest.fixture(name="session")
def session_fixture():
    """provides a sqlite in-memory database that substitutes the main postgres db for testing purposes"""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture(name="cache")
def cache_fixture():
    """provides a redis cache for testing"""
    cache = Redis(host="localhost", port=6379, db=3)
    yield cache
    cache.flushdb()
    cache.close()


@pytest.fixture(name="client")
def client_fixture(session: Session, cache: Redis):
    """provides a test client with the session and overrides prod session and cache providers to test safely"""

    def get_session_override():
        return session

    def get_redis_client_override():
        return cache

    app.dependency_overrides[get_db_session] = get_session_override
    app.dependency_overrides[get_redis_client] = get_redis_client_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


## end shared fixtures
