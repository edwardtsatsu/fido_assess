from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from fastapi_pagination import Params, create_page

from src.response.user_response import UserResponse
from src.constants.transaction_type import TransactionType
from src.response.transaction_response import TransactionResponse
from src.services.transaction_service import TransactionService
from src.tasks import (
    alert_relevant_systems,
    calculate_credit_score,
    invalidate_transactions_cache,
    update_user_statistics,
)


@pytest.fixture
def transaction_service():
    trans_repo_mock = MagicMock()
    background_tasks_mock = MagicMock()
    redis_service_mock = MagicMock()

    return TransactionService(
        trans_repo=trans_repo_mock,
        background_task=background_tasks_mock,
        redis_service=redis_service_mock,
    )


def _test_find_all_with_cache(transaction_service):
    cached_data = {
        "items": [
            '{"full_name": "test test", "date": "2023-10-01T12:00:00", "type": "credit", "user_id": 1}'
        ],
        "page": 1,
        "size": 10,
        "total": 1,
    }
    transaction_service.redis_service.retrieve_from_cache.return_value = cached_data

    query = {"page": 1, "size": 10, "user_id": 1}
    response = transaction_service.find_all(query)

    assert len(response.items) == 1
    assert response.items[0].user.first_name == "test"
    assert response.items[0].type == TransactionType.CREDIT
    transaction_service.redis_service.retrieve_from_cache.assert_called_once_with(
        "items_page_1_size_10_user_1"
    )


def _test_find_all_without_cache(transaction_service):
    transaction_service.redis_service.retrieve_from_cache.return_value = None
    transaction_service.repository.find_all.return_value = create_page(
        [
            TransactionResponse(
                id=1,
                amount=100,
                date=datetime.now(),
                type=TransactionType.CREDIT,
                user={"id": 1, "first_name": "test", "last_name": "test"},
            )
        ],
        params=Params(page=1, size=10),
        total=1,
    )

    query = {"page": 1, "size": 10, "user_id": 1}
    response = transaction_service.find_all(query)

    assert len(response.items) == 1
    assert response.items[0].user.first_name == "test"
    assert response.items[0].type == TransactionType.CREDIT
    transaction_service.repository.find_all.assert_called_once_with(query)
    transaction_service.redis_service.store_in_cache.assert_called_once()


def test_store(transaction_service):
    # given
    data = {
        "amount": 10,
        "type": TransactionType.CREDIT,
        "user_id": 1,
        "exttrid": "swgkjgwdqhfj",
        "date": "2024-10-06T20:20:30.964Z",
        "description": "Test transaction",
    }

    user_mock = UserResponse(
        id=1, first_name="test", last_name="test", full_name="test test"
    )

    transaction_response_mock = TransactionResponse(
        id=1,
        amount=10,
        date=datetime.now(),
        type=TransactionType.CREDIT,
        user=user_mock,
        exttrid="swgkjgwdqhfj",
        description="Test transaction",
        user_id=1,
        created_at=datetime.now(),
    )

    transaction_service.store = MagicMock(return_value=transaction_response_mock)
    transaction_service.perform_background_tasks = MagicMock()

    # when
    response = transaction_service.store(data)

    # expected
    assert response.id == transaction_response_mock.id
    assert response.user.first_name == transaction_response_mock.user.first_name
    assert response.user.last_name == transaction_response_mock.user.last_name
    assert response.amount == transaction_response_mock.amount
    assert response.type == transaction_response_mock.type
    assert response.exttrid == transaction_response_mock.exttrid
    assert response.description == transaction_response_mock.description

    transaction_service.store.assert_called_once_with(data)


def _test_fetch_analytics_with_cache(transaction_service):
    cached_analytics = {
        "avg_amount": 100,
        "total_credit": 200,
        "total_debit": 50,
        "highest_trans_date": "2023-10-01",
    }
    transaction_service.redis_service.retrieve_from_cache.return_value = (
        cached_analytics
    )

    query = {"user_id": 1}
    response = transaction_service.fetch_analytics(query)

    assert response.avg_amount == 100
    assert response.total_credit == 200
    assert response.highest_trans_date == "2023-10-01"
    transaction_service.redis_service.retrieve_from_cache.assert_called_once_with(
        "analytics_1"
    )


def _test_fetch_analytics_without_cache(transaction_service):
    transaction_service.redis_service.retrieve_from_cache.return_value = None
    transaction_service.trans_repo.find_avg_and_total_trans.return_value = (
        100,
        200,
        50,
    )
    transaction_service.trans_repo.highest_trans_date.return_value = datetime.now()

    query = {"user_id": 1}
    response = transaction_service.fetch_analytics(query)

    assert response.avg_amount == 100
    assert response.total_credit == 200
    transaction_service.redis_service.store_in_cache.assert_called_once()


def _test_perform_background_tasks(transaction_service):
    mock_transaction_response = TransactionResponse(
        id=1,
        amount=100,
        date=datetime.now(),
        type=TransactionType.CREDIT,
        user={"id": 1, "first_name": "test", "last_name": "test"},
    )

    transaction_service.perform_background_tasks(mock_transaction_response)

    transaction_service.background_task.add_task.assert_any_call(
        calculate_credit_score, mock_transaction_response
    )
    transaction_service.background_task.add_task.assert_any_call(
        alert_relevant_systems, mock_transaction_response
    )
    transaction_service.background_task.add_task.assert_any_call(
        update_user_statistics,
        mock_transaction_response,
        transaction_service.calculate_analytics,
    )
    transaction_service.background_task.add_task.assert_any_call(
        invalidate_transactions_cache,
        mock_transaction_response.user["id"],
        transaction_service.redis_service,
    )
