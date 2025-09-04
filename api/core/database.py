from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from api.core.settings import Settings

# w key reference
engine = create_engine(Settings().DATABASE_URL)


def get_session():
    """
    Function to create a session in Settings.DATABASE_URL
    Yields:
        session: A SQLAlchemy object request
    """
    with Session(engine) as session:
        yield session
