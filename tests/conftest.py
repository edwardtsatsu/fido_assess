# tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configs.database import Base
from src.models.user import User

# Test database URL for SQLite
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create a new SQLAlchemy engine
engine = create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_session():
    """Create a new database session for a test."""
    # Create the database tables for testing
    Base.metadata.create_all(bind=engine)

    # Create a new session for the test
    db = SessionLocal()
    yield db

    # Cleanup
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def clean_db(db_session):
    """Clean the database after each test."""
    yield
    db_session.query(User).delete()
    db_session.commit()
