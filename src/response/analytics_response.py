from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AnalyticsResponse(BaseModel):
    avg_amount: float
    total_credit: float
    total_debit: float

    model_config = ConfigDict(from_attributes=True)
