import redis
import json
import os

REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://localhost:6379"
)

redis_client = redis.Redis.from_url(
    REDIS_URL,
    decode_responses=True
)


def enqueue_task(task_name: str, data: dict):

    task = {
        "task": task_name,
        "data": data
    }

    redis_client.rpush(
        "flowforge_queue",
        json.dumps(task)
    )
