from dependency_injector import containers, providers

from avia.application.usecases.user.auth.login import Login
from avia.application.usecases.user.create import CreateUser
from avia.infrastructure.depends.repos_container import ReposContainer
from avia.infrastructure.jwt.jwt_config import JwtConfig
from avia.infrastructure.jwt.jwt_processor import JwtProcessor
from avia.infrastructure.security.password_hasher import PasswordHasher


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
        CreateUser,
        user_repository=ReposContainer.user_repository,
        password_hasher=password_hasher,
    )
