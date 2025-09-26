from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from api.core.settings import Settings

# w key reference
engine = create_async_engine(Settings().DATABASE_URL)


async def get_session():
    """
    Function to create an async session in Settings.DATABASE_URL
    Yields:
        session: An Async SQLAlchemy object request
    """
    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session
