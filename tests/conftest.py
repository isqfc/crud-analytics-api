import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api.app import app
from api.core.models import User, table_registry

# w key reference


@pytest.fixture
def client():
    """
    Arrange fixture - (AAA)
    Yields:
          Client to use HTTP requests
    """
    def dependency_override():
        return session

    with TestClient(app) as app_request:
        app.dependency_overrides = dependency_override()
        yield app_request

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    """
    Create a session with table_registry metadata in memory for tests
    Yields:
          A SQLAlchemy session request
    """
    engine = create_engine('sqlite:///memory:')

    with Session(engine) as session_request:
        table_registry.metadata.create_all()
        yield session_request

    table_registry.metadata.drop_all()
    engine.dispose()


@pytest.fixture
def user(session):

    model = User(
        username=fake_user.username,
        email=fake_user.email,
        password=fake_user.password
    )

    session.add(model)
    session.commit()
    session.refresh(model)

    return model


# Faker uses below
fake = Faker(locale='pt_BR')
Faker.seed(0)

fake_user = {
    'id': 1,
    'username': fake.name.unique(),
    'email': fake.email.unique(),
    'password': fake.password.unique()
}


@pytest.fixture
def input_user():
    user = fake_user.copy()
    user.pop(id)
    return user


@pytest.fixture
def output_user():
    user = fake_user.copy()
    user.pop('password')
    return user
