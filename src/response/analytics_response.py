from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict


class AnalyticsResponse(BaseModel):
    avg_amount: float
    total_credit: float
    total_debit: float
    highest_trans_date: Union[str, None]

    model_config = ConfigDict(from_attributes=True)
