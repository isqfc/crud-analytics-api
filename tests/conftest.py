import pytest_asyncio
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from api.app import app
from api.auth.utils import create_access_token, get_password_hash
from api.core.database import get_session
from api.core.models import User, table_registry

# w key reference


@pytest_asyncio.fixture
async def client(session):
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


@pytest_asyncio.fixture
async def session():
    """
    Create a session with table_registry metadata in memory for tests
    Yields:
          A Async SQLAlchemy session request
    """
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool
        )
    async with engine.begin() as connection:
        await connection.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session_request:
        yield session_request
        await session_request.close()

    async with engine.begin() as connection:
        await connection.run_sync(table_registry.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
def access_token():
    return create_access_token


# Fixture to inject fake_user on sqlite database in memory and returns user
@pytest_asyncio.fixture
async def user(session):

    model = User(
        username=fake_user['username'],
        email=fake_user['email'],
        password=get_password_hash(fake_user['password'])
    )

    session.add(model)
    await session.commit()
    await session.refresh(model)

    model.plain_password = fake_user['password']
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


@pytest_asyncio.fixture
def input_user():
    user = fake_user.copy()
    user.pop('id')
    return user


@pytest_asyncio.fixture
def output_user():
    user = fake_user.copy()
    user.pop('password')
    return user
