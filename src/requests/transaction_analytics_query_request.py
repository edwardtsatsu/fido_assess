import uuid
from datetime import date
from typing import Optional, Union

from fastapi import Query
from pydantic import BaseModel


class TransactionAnalyticsQueryRequest(BaseModel):
    user_id: int
    start_date: Optional[date] = Query(default=None)
    end_date: Optional[date] = Query(default=None)
