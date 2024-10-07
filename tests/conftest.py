import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configs.database import Base
from src.models.user import User

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db_session():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    yield db

    # Cleanup
    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def clean_db(db_session):
    yield
    db_session.query(User).delete()
    db_session.commit()
