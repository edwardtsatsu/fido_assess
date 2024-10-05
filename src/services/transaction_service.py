from abc import ABC

from fastapi import Depends

from src.response.analytics_response import AnalyticsResponse
from src.repositories.transaction_repository import TransactionRepository
from src.response.transaction_response import TransactionResponse
from src.services.base_service import BaseService
from src.utils import convert_to_pesewas


class TransactionService(BaseService, ABC):

    def __init__(
        self, trans_repo: TransactionRepository = Depends(TransactionRepository)
    ):
        super().__init__(repository=trans_repo)

    def get_response(self):
        return TransactionResponse

    def store(self, data):
        data["amount"] = convert_to_pesewas(data["amount"])
        return super().store(data)

    def fetch_analytics(self, query):
        result = self.repository.find_avg_and_total_trans(query["user_id"])
        return AnalyticsResponse(
            avg_amount=result[0],
            total_credit=result[1],
            total_debit=result[2],
        )
