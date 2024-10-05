import time

from src.response.transaction_response import TransactionResponse
from src.services.redis_service import RedisService


def calculate_credit_score(data: TransactionResponse):
    print(f"Calculating credit score for user with id: {data.user_id}")
    print("completed credit")


def alert_relevant_systems(data: TransactionResponse):
    print(f"alerting relevant system for user id: {data.user_id}")
    print("completed relevant")


def update_user_statistics(data: TransactionResponse, calculate_analytics):
    print(f"updating user statistics for user with id: {data.user_id}")
    calculate_analytics(data.user_id)
    print("completed update of user statistics")


def invalidate_transactions_cache(user_id: str, redis_service: RedisService):
    print(f"invalidating cache: {user_id}")
    cached_keys = redis_service.fetch_keys_by_pattern(
        f"items_page_*_size_*_user_{user_id}"
    )

    for key in cached_keys:
        redis_service.remove_from_cache(key)
