import json
from abc import ABC
from datetime import datetime
from typing import Annotated

from fastapi import BackgroundTasks, Depends
from fastapi_pagination import Params, create_page

from configs.logger import logger
from src.constants.transaction_type import TransactionType
from src.exceptions.user_not_found_exception import UserNotFoundException
from src.repositories.transaction_repository import TransactionRepository
from src.repositories.user_repository import UserRepository
from src.response.analytics_response import AnalyticsResponse
from src.response.transaction_response import TransactionResponse
from src.response.user_response import UserResponse
from src.services.base_service import BaseService
from src.services.redis_service import RedisService
from src.tasks import (
    alert_relevant_systems,
    calculate_credit_score,
    invalidate_transactions_cache,
    update_user_statistics,
)
from src.utils import convert_to_cedis


class TransactionService(BaseService, ABC):

    def __init__(
        self,
        trans_repo: Annotated[TransactionRepository, Depends(TransactionRepository)],
        user_repo: Annotated[UserRepository, Depends(UserRepository)],
        background_task: BackgroundTasks,
        redis_service: Annotated[RedisService, Depends(RedisService)],
    ):
        super().__init__(repository=trans_repo)
        self.background_task = background_task
        self.trans_repo = trans_repo
        self.redis_service = redis_service
        self.user_repo = user_repo

    def get_response(self):
        return TransactionResponse

    def find_all(self, query=None):
        page = query["page"]
        size = query["size"]
        key = f"items_page_{page}_size_{size}_user_{query['user_id']}"

        cached_data = self.redis_service.retrieve_from_cache(key)

        if cached_data:
            items = []
            for json_item in cached_data["items"]:
                item = json.loads(json_item)
                names = item["full_name"].split(" ")
                item["date"] = datetime.fromisoformat(item["date"])
                item["type"] = (
                    TransactionType.CREDIT
                    if item["type"] == "credit"
                    else TransactionType.DEBIT
                )

                items.append(
                    TransactionResponse(
                        **item,
                        user=UserResponse(
                            id=item["user_id"], first_name=names[0], last_name=names[1]
                        ),
                    )
                )

            return create_page(
                items,
                params=Params(page=cached_data["page"], size=cached_data["size"]),
                total=cached_data["total"],
            )

        logger.info("Performing request to db, when cache is invalidated..")

        transactions = self.repository.find_all(query)
        items = dict(transactions)
        items["items"] = [item.model_dump_json() for item in transactions.items]

        self.redis_service.store_in_cache(key, items)

        return transactions

    def store(self, data):
        user = self.user_repo.find(data["user_id"])
        if user is None:
            raise UserNotFoundException(description="User not found")
        resource = super().store(data)
        self.perform_background_tasks(resource)
        return resource

    def fetch_analytics(self, query):
        user_id = query["user_id"]
        
        analytics = self.redis_service.retrieve_from_cache(f"analytics_{user_id}")

        if analytics is not None:
            return AnalyticsResponse(**analytics)

        return self.calculate_analytics(user_id)

    def perform_background_tasks(self, resource: TransactionResponse):
        # perform credit score asynchronously
        self.background_task.add_task(calculate_credit_score, resource)

        # alert relevant systems
        self.background_task.add_task(alert_relevant_systems, resource)

        # update cache
        self.background_task.add_task(
            update_user_statistics, resource, self.calculate_analytics
        )
        # invalidate cache
        self.background_task.add_task(
            invalidate_transactions_cache, resource.user_id, self.redis_service
        )

    def delete(self, id):
        resource = super().delete(id)
        self.background_task.add_task(
            invalidate_transactions_cache, resource.user_id, self.redis_service
        )

    def calculate_analytics(self, user_id):
        result = self.trans_repo.find_avg_and_total_trans(user_id)
        trans_date = self.trans_repo.highest_trans_date(user_id)

        analytics = AnalyticsResponse(
            avg_amount=convert_to_cedis(result[0]),
            total_credit=convert_to_cedis(result[1]),
            total_debit=convert_to_cedis(result[2]),
            highest_trans_date=(
                trans_date.strftime("%Y-%m-%d") if trans_date is not None else None
            ),
        )

        # store in cache
        self.redis_service.store_in_cache(
            f"analytics_{user_id}", analytics.model_dump()
        )

        return analytics
