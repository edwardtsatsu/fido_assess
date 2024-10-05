import json
from typing import Optional

from fastapi import Depends

from configs.redis import get_redis_instance


class RedisService:
    def __init__(self, redis_client=Depends(get_redis_instance)):
        self.redis_client = redis_client

    def store_in_cache(self, key: str, value: dict, expiration: int = 300) -> None:
        self.redis_client.setex(key, expiration, json.dumps(value))

    def retrieve_from_cache(self, key: str) -> Optional[dict]:
        cached_value = self.redis_client.get(key)
        if cached_value is None:
            return None
        return json.loads(cached_value)

    def remove_from_cache(self, key: str) -> None:
        self.redis_client.delete(key)

    def fetch_keys_by_pattern(self, pattern: str):
        matched_keys = []
        cursor = "0"

        while cursor != 0:
            cursor, keys = self.redis_client.scan(cursor=cursor, match=pattern)
            matched_keys.extend(keys)

        return matched_keys
