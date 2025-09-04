import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from api.app import app
from api.core.database import get_session
from api.core.models import User, table_registry

# w key reference


@pytest.fixture
def client(session):
    """
    Arrange fixture - (AAA)
    Yields:
          Client to use HTTP requests
    """
    def dependency_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = dependency_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    """
    Create a session with table_registry metadata in memory for tests
    Yields:
          A SQLAlchemy session request
    """
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
        )

    table_registry.metadata.create_all(engine)
    with Session(engine) as session_request:
        yield session_request
        session_request.close()

    table_registry.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def user(session):

    model = User(
        username=fake_user['username'],
        email=fake_user['email'],
        password=fake_user['password']
    )

    session.add(model)
    session.commit()
    session.refresh(model)

    return model


# Faker user below
fake = Faker(locale='pt_BR')
Faker.seed(0)

fake_user = {
    'id': 1,
    'username': fake.unique.name(),
    'email': fake.unique.email(),
    'password': fake.unique.password()
}


@pytest.fixture
def input_user():
    user = fake_user.copy()
    user.pop('id')
    return user


@pytest.fixture
def output_user():
    user = fake_user.copy()
    user.pop('password')
    return user
