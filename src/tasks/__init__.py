import time

from configs.logger import logger
from src.response.transaction_response import TransactionResponse
from src.services.redis_service import RedisService


def calculate_credit_score(data: TransactionResponse):
    logger.info(f"Calculating credit score for user with id: {data.user_id}")
    logger.info("completed credit")


def alert_relevant_systems(data: TransactionResponse):
    logger.info(f"alerting relevant system for user id: {data.user_id}")
    logger.info("completed relevant")


def update_user_statistics(data: TransactionResponse, calculate_analytics):
    logger.info(f"updating user statistics for user with id: {data.user_id}")
    calculate_analytics(data.user_id)
    logger.info("completed update of user statistics")


def invalidate_transactions_cache(user_id: str, redis_service: RedisService):
    logger.info(f"invalidating cache: {user_id}")
    cached_keys = redis_service.fetch_keys_by_pattern(
        f"items_page_*_size_*_user_{user_id}"
    )

    for key in cached_keys:
        redis_service.remove_from_cache(key)
