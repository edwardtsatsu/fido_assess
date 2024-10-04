from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from configs import settings
from src.models.base import Base


engine = create_engine(f"postgresql+psycopg2://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}")
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base.query = db_session.query_property()
