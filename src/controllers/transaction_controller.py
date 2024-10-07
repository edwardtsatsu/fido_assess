from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from starlette import status
from typing_extensions import Annotated

from src.requests.transaction_analytics_query_request import (
    TransactionAnalyticsQueryRequest,
)
from src.requests.transaction_query_request import TransactionQueryRequest
from src.requests.transaction_request import TransactionRequest
from src.response.transaction_response import TransactionResponse
from src.services.transaction_service import TransactionService

transaction_router = APIRouter(tags=["Transaction"])


@transaction_router.post(
    "", summary="Save a transaction", status_code=status.HTTP_201_CREATED
)
async def store(
    transaction_request: TransactionRequest,
    service: Annotated[TransactionService, Depends(TransactionService)],
) -> TransactionResponse:
    """
    Create a new transaction.

    - **transaction_request**: The payload containing details about the transaction.
        - **user_id**: ID of the user for whom the transaction is being created.
        - **amount**: The transaction amount.
        - **exttrid**: External transaction ID for tracking.
        - **date**: Date of the transaction.
        - **type**: Type of the transaction (e.g., credit or debit).
        - **description**: Description or note about the transaction.

    Returns the newly created transaction details as a `TransactionResponse`.
    """
    return service.store(transaction_request.model_dump())


@transaction_router.get(
    "", summary="List all transactions", response_model=Page[TransactionResponse]
)
async def find_all(
    service: Annotated[TransactionService, Depends(TransactionService)],
    query: Annotated[TransactionQueryRequest, Depends(TransactionQueryRequest)],
):
    """
    Fetch a paginated list of transactions.

    - **query**: Query parameters used to filter the list of transactions.
        - **user_id**: Filter by user ID (required).

    Returns a paginated list of `TransactionResponse`, using the `Page` response model which includes:
        - **items**: A list of transactions on the current page.
        - **total**: Total number of transactions.
        - **page**: The current page number.
        - **size**: The number of transactions per page.
    """
    data = query.model_dump()
    return service.find_all(data)


@transaction_router.delete(
    "/{id}", summary="Delete a transaction", status_code=status.HTTP_204_NO_CONTENT
)
async def destroy(
    id: int,
    service: Annotated[TransactionService, Depends(TransactionService)],
) -> None:
    """
    Delete a transaction by ID.

    - **id**: The ID of the transaction to delete.

    Returns nothing on success, but the transaction will be deleted from the database.
    """
    return service.delete(id)


@transaction_router.get("/analytics", summary="Fetch transaction analytics")
async def analytics(
    service: Annotated[TransactionService, Depends(TransactionService)],
    query: Annotated[
        TransactionAnalyticsQueryRequest, Depends(TransactionAnalyticsQueryRequest)
    ],
):
    """
    Fetch analytics for transactions.

    - **query**: Query parameters used to fetch transaction analytics.
        - **user_id**: Filter analytics by user (optional).

    Returns transaction statistics based on the query.
    """
    data = query.model_dump()
    return service.fetch_analytics(data)
