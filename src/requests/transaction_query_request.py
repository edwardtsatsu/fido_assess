import uuid
from typing import Optional, Union

from fastapi import Query
from pydantic import BaseModel


class TransactionQueryRequest(BaseModel):
    user_id: int
    page: int = Query(1, ge=1)
    size: int = Query(50, ge=1)
