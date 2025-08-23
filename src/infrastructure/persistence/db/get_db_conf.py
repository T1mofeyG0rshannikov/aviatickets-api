from functools import lru_cache

from src.infrastructure.persistence.db.db_config import DbConfig


@lru_cache
def get_db_config() -> DbConfig:
    return DbConfig()
