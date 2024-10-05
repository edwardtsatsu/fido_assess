from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from configs import settings
from src.models.base import Base

engine = create_engine(
    f"postgresql://{settings.database_user}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
)

DbSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(DbSession)


def get_db():
    db = DbSession()
    try:
        yield db
    finally:
        db.close()
