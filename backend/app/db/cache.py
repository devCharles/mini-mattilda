import os

from redis import Redis

redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_db = int(os.getenv("REDIS_DB", 0))

redis_client: Redis | None = None


def redis_connect(host=redis_host, port=redis_port, db=redis_db):
    global redis_client
    if redis_client is None:
        print("Connecting Redis")
        redis_client = Redis(host=host, port=port, db=db)
    return redis_client


def get_redis_client(host=redis_host, port=redis_port, db=redis_db):
    with redis_connect(host=host, port=port, db=db) as client:
        yield client


def redis_disconnect():
    global redis_client
    if redis_client is not None:
        print("Disconnecting from Redis")
        redis_client.close()
        redis_client = None
