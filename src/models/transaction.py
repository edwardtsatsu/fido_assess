from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime
from sqlalchemy import Enum as SQLALchemyEnum
from sqlalchemy import ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import relationship

from src.models.base import Base
from src.constants.transaction_type import TransactionType


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    amount = Column(Numeric(10, 2), nullable=False)
    type = Column(SQLALchemyEnum(TransactionType), nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    del_status = Column(Boolean, default=False, nullable=False)
    updated_at = Column(DateTime, server_onupdate=func.now(), nullable=True)

    user = relationship("User", back_populates="transactions")
