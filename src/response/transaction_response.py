from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field

from src.constants.transaction_type import TransactionType
from src.response.user_response import UserResponse


class TransactionResponse(BaseModel):
    id: int
    date: datetime
    amount: float
    exttrid: str
    type: TransactionType
    description: str
    user_id: int
    user: UserResponse = Field(exclude=True)
    created_at: Optional[datetime] = None

    @computed_field
    def full_name(self) -> str:
        if self.user is None:
            return None
        return f"{self.user.first_name} {self.user.last_name}"

    model_config = ConfigDict(from_attributes=True)
