import redis

from configs import settings


def get_redis_instance():
    return redis.Redis(
        host=settings.redis_host, port=settings.redis_port, db=0, decode_responses=True
    )
