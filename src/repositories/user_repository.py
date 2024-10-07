from fastapi import Depends
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from configs.database import get_db
from src.models.user import User
from src.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, db_session: Annotated[Session, Depends(get_db)]):
        super().__init__(model=User, db_session=db_session)
