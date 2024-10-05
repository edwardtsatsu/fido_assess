import uuid
from typing import Optional, Union

from fastapi import Query
from pydantic import BaseModel


class TransactionQueryRequest(BaseModel):
    user_id: Optional[int] = Query(None)
