from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, field_validator
from sqlalchemy import select

from configs.database import db_session, get_db
from src.constants.transaction_type import TransactionType
from src.models.transaction import Transaction
from src.models.user import User
from src.utils import convert_to_pesewas


class TransactionRequest(BaseModel):
    user_id: int
    amount: float
    exttrid: str
    date: datetime
    type: TransactionType
    description: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("user_id")
    def user_exist(cls, v):
        user = (
            next(get_db())
            .scalars(select(User).where(User.id == v).where(User.active_status == True))
            .first()
        )
        if user is None:
            raise ValueError("User not found")
        return v

    @field_validator("amount")
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Transaction amount must be greater than 0")
        return convert_to_pesewas(v)

    @field_validator("exttrid")
    def unique_transaction(cls, v):
        transaction = (
            next(get_db())
            .scalars(select(Transaction).where(Transaction.exttrid == v))
            .first()
        )
        if transaction is not None:
            raise ValueError("transaction id already exist")
        return v
