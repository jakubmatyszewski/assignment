import pytest

from copy import deepcopy
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import Base, schemas
from app.db.database import get_db, create_user
from app.utils.login import login_manager

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

test_user = schemas.User(
    **{"username": "test_user", "pseudonym": "Bob", "password": "Hush", "enabled": True}
)


@pytest.fixture
def basic_user_schema():
    return test_user


db = next(override_get_db())
user_ORM = create_user(test_user, db)


@pytest.fixture
def client():
    """
    Return an API Client
    """
    app.dependency_overrides = {}
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def client_authenticated():
    """
    Returns an API client where user is logged in
    """

    def authorized():
        return test_user

    app.dependency_overrides[login_manager] = authorized
    return TestClient(app)


@pytest.fixture
def client_authenticated_villain():
    """
    Returns an API client where user is logged in
    """

    def authorized():
        villain = deepcopy(test_user)
        villain.username = "Darth Vader"
        return villain


    app.dependency_overrides[login_manager] = authorized
    return TestClient(app)
