import pytest
from redis import Redis

from src.infrastructure.depends.base import get_redis_config
from src.infrastructure.redis.config import RedisConfig


@pytest.fixture
def redis(config: RedisConfig = get_redis_config()) -> Redis:
    return Redis(host=config.host, port=config.port, db=config.db, decode_responses=True)
