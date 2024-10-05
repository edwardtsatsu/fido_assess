from abc import ABC

from fastapi import Depends

from src.response.analytics_response import AnalyticsResponse
from src.repositories.transaction_repository import TransactionRepository
from src.response.transaction_response import TransactionResponse
from src.services.base_service import BaseService
from src.utils import convert_to_cedis


class TransactionService(BaseService, ABC):

    def __init__(
        self, trans_repo: TransactionRepository = Depends(TransactionRepository)
    ):
        super().__init__(repository=trans_repo)

    def get_response(self):
        return TransactionResponse

    def fetch_analytics(self, query):
        user_id = query["user_id"]
        result = self.repository.find_avg_and_total_trans(user_id)
        trans_date = self.repository.highest_trans_date(user_id)
        return AnalyticsResponse(
            avg_amount=convert_to_cedis(result[0]),
            total_credit=convert_to_cedis(result[1]),
            total_debit=convert_to_cedis(result[2]),
            highest_trans_date=trans_date.strftime("%Y-%m-%d"),
        )
