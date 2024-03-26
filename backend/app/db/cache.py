import os
from redis import Redis

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_db = int(os.getenv("REDIS_DB", 0))

redis_client: Redis | None = None


def redis_connect():
    global redis_client
    if redis_client is None:
        print("Connecting Redis")
        redis_client = Redis(host=redis_host, port=redis_port, db=redis_db)
    return redis_client


def get_redis_client():
    with redis_connect() as client:
        yield client


def redis_disconnect():
    global redis_client
    if redis_client is not None:
        print("Disconnecting from Redis")
        redis_client.close()
        redis_client = None
