from datetime import datetime
from typing import Optional, Union

from pydantic import (BaseModel, ConfigDict, Field, computed_field,
                      field_serializer)

from src.constants.transaction_type import TransactionType
from src.response.user_response import UserResponse
from src.utils import convert_to_cedis, decrypt_text


class TransactionResponse(BaseModel):
    id: int
    date: datetime
    amount: float
    exttrid: str
    type: TransactionType
    description: str
    user_id: int
    user: UserResponse = Field(exclude=True)
    created_at: Union[datetime, None]

    @computed_field
    def full_name(self) -> str:
        if self.user is None:
            return None
        return self.user.full_name

    @field_serializer("amount")
    def formatted_amount(self, amount) -> float:
        return convert_to_cedis(amount)

    model_config = ConfigDict(from_attributes=True)
