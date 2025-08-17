from typing import Annotated

from src.depends.decorator import inject_dependencies
from src.depends.depends import get_jwt_config, get_password_hasher
from src.depends.repos_container import ReposContainer
from src.infrastructure.jwt.jwt_config import JwtConfig
from src.infrastructure.jwt.jwt_processor import JwtProcessor
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.security.password_hasher import PasswordHasher
from src.usecases.user.login import Login


def get_jwt_processor(config: JwtConfig = get_jwt_config()) -> JwtProcessor:
    return JwtProcessor(config)


@inject_dependencies
async def get_login_interactor(
    user_repository: Annotated[UserRepository, ReposContainer.user_repository],
    jwt_processor: Annotated[JwtProcessor, get_jwt_processor],
    password_hasher: Annotated[PasswordHasher, get_password_hasher],
) -> Login:
    return Login(user_repository, jwt_processor, password_hasher)
