import pytest

from avia.infrastructure.jwt.jwt_config import JwtConfig
from avia.infrastructure.jwt.jwt_processor import JwtProcessor
from avia.infrastructure.security.password_hasher import PasswordHasher


@pytest.fixture
async def password_hasher() -> PasswordHasher:
    return PasswordHasher()


@pytest.fixture
def jwt_settings() -> JwtConfig:
    return JwtConfig()


@pytest.fixture
async def jwt_processor(jwt_settings: JwtConfig) -> JwtProcessor:
    return JwtProcessor(jwt_settings)
