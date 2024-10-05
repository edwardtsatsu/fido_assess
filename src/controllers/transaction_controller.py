import uuid

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from starlette import status
from typing_extensions import Annotated

from src.requests.transaction_analytics_query_request import \
    TransactionAnalyticsQueryRequest
from src.requests.transaction_query_request import TransactionQueryRequest
from src.requests.transaction_request import TransactionRequest
from src.response.transaction_response import TransactionResponse
from src.services.transaction_service import TransactionService

transaction_router = APIRouter(tags=["Transaction"])


@transaction_router.post("", status_code=status.HTTP_201_CREATED)
async def store(
    transaction_request: TransactionRequest,
    service: Annotated[TransactionService, Depends(TransactionService)],
) -> TransactionResponse:
    return service.store(transaction_request.model_dump())


@transaction_router.get("", response_model=Page[TransactionResponse])
async def find_all(
    service: Annotated[TransactionService, Depends(TransactionService)],
    query: Annotated[TransactionQueryRequest, Depends(TransactionQueryRequest)],
):
    data = query.model_dump()
    return service.find_all(data)


@transaction_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(
    id, service: Annotated[TransactionService, Depends(TransactionService)]
) -> None:
    return service.delete(id)


@transaction_router.get("/analytics")
async def analytics(
    service: Annotated[TransactionService, Depends(TransactionService)],
    query: Annotated[
        TransactionAnalyticsQueryRequest, Depends(TransactionAnalyticsQueryRequest)
    ],
):
    data = query.model_dump()
    return service.fetch_analytics(data)
