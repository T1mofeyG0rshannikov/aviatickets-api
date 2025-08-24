from dependency_injector import containers, providers

from src.application.usecases.user.auth.login import Login
from src.infrastructure.depends.repos_container import ReposContainer
from src.infrastructure.jwt.jwt_config import JwtConfig
from src.infrastructure.jwt.jwt_processor import JwtProcessor
from src.infrastructure.security.password_hasher import PasswordHasher


class UsecasesDIContainer(containers.DeclarativeContainer):
    jwt_config = providers.Singleton(JwtConfig)
    jwt_processor = providers.Singleton(JwtProcessor, jwt_config)
    password_hasher = providers.Singleton(PasswordHasher)

    login = providers.Factory(
        Login,
        user_repository=ReposContainer.user_repository,
        jwt_processor=jwt_processor,
        password_hasher=password_hasher,
    )

    create_user = providers.Factory(
        user_repository=ReposContainer.user_repository,
        password_hasher=password_hasher,
    )
