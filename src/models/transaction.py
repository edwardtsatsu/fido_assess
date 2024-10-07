from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Index,
    UniqueConstraint,
)
from sqlalchemy import Enum as SQLALchemyEnum
from sqlalchemy import ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from src.constants.transaction_type import TransactionType
from src.models.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    date = Column(DateTime)
    exttrid = Column(String, nullable=False, unique=True)
    amount = Column(Integer, nullable=False)
    type = Column(SQLALchemyEnum(TransactionType), nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)
    del_status = Column(Boolean, default=False, nullable=False)
    updated_at = Column(DateTime, server_onupdate=func.now(), nullable=True)

    user = relationship("User", back_populates="transactions")

    __table_args__ = (
        UniqueConstraint("exttrid", name="uq_exttrid"),
        CheckConstraint("amount > 0", name="check_amount_positive"),
        Index("idx_user_id", "user_id"),
        Index("idx_exttrid", "exttrid"),
        Index("idx_date", "date"),
    )
