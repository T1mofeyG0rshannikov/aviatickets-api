from functools import lru_cache

from src.infrastructure.db.db_config import DbConfig


@lru_cache
def get_db_config() -> DbConfig:
    return DbConfig()
