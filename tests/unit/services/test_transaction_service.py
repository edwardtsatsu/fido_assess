from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.exceptions.user_not_found_exception import UserNotFoundException
from src.constants.transaction_type import TransactionType
from src.models.transaction import Transaction
from src.models.user import User
from src.response.transaction_response import TransactionResponse
from src.services.transaction_service import TransactionService


def test_store_should_return_transaction_response():
    trans_repo_mock = MagicMock()
    background_tasks_mock = MagicMock()
    redis_service_mock = MagicMock()
    user_repo_mock = MagicMock()

    transaction_service = TransactionService(
        trans_repo=trans_repo_mock,
        background_task=background_tasks_mock,
        redis_service=redis_service_mock,
        user_repo=user_repo_mock,
    )

    data = {
        "amount": 10,
        "type": TransactionType.CREDIT,
        "user_id": 1,
        "exttrid": "swgkjgwdqhfj",
        "date": "2024-10-06T20:20:30.964Z",
        "description": "Test transaction",
    }

    user_resp_mock = User(id=1, first_name="test", last_name="test")

    transaction_response_mock = Transaction(
        id=1,
        amount=10,
        date=datetime.now(),
        type=TransactionType.CREDIT,
        user=user_resp_mock,
        exttrid="swgkjgwdqhfj",
        description="Test transaction",
        user_id=1,
        created_at=datetime.now(),
    )

    trans_repo_mock.store = MagicMock(return_value=transaction_response_mock)
    user_repo_mock.find = MagicMock(return_value=user_resp_mock)

    actual = transaction_service.store(data)

    expected = TransactionResponse(
        id=transaction_response_mock.id,
        amount=transaction_response_mock.amount,
        date=transaction_response_mock.date,
        type=transaction_response_mock.type,
        user=user_resp_mock,
        created_at=transaction_response_mock.created_at,
        user_id=transaction_response_mock.user_id,
        exttrid=transaction_response_mock.exttrid,
        description=transaction_response_mock.description,
    )

    assert actual == expected



def test_store_should_raise_user_exception_not_found_exception():
    trans_repo_mock = MagicMock()
    background_tasks_mock = MagicMock()
    redis_service_mock = MagicMock()
    user_repo_mock = MagicMock()

    transaction_service = TransactionService(
        trans_repo=trans_repo_mock,
        background_task=background_tasks_mock,
        redis_service=redis_service_mock,
        user_repo=user_repo_mock,
    )

    data = {
        "amount": 10,
        "type": TransactionType.CREDIT,
        "user_id": 1,
        "exttrid": "swgkjgwdqhfj",
        "date": "2024-10-06T20:20:30.964Z",
        "description": "Test transaction",
    }

    user_repo_mock.find = MagicMock(return_value=None)

    with pytest.raises(UserNotFoundException):
        transaction_service.store(data)
