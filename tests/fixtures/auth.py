import pytest

from src.infrastructure.jwt.jwt_config import JwtConfig
from src.infrastructure.jwt.jwt_processor import JwtProcessor
from src.infrastructure.security.password_hasher import PasswordHasher


@pytest.fixture
async def password_hasher() -> PasswordHasher:
    return PasswordHasher()


@pytest.fixture
def jwt_settings() -> JwtConfig:
    return JwtConfig()


@pytest.fixture
async def jwt_processor(jwt_settings: JwtConfig) -> JwtProcessor:
    return JwtProcessor(jwt_settings)
