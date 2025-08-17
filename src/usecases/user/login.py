from src.entities.exceptions import AccessDeniedError
from src.entities.user.access_token import AccessToken
from src.entities.user.exceptions import InvalidPasswordError, UserNotFoundError
from src.infrastructure.jwt.jwt_processor import JwtProcessor
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.security.password_hasher import PasswordHasher


class Login:
    def __init__(
        self, user_repository: UserRepository, jwt_processor: JwtProcessor, password_hasher: PasswordHasher
    ) -> None:
        self.user_repository = user_repository
        self.jwt_processor = jwt_processor
        self.password_hasher = password_hasher

    async def __call__(self, email: str, password: str, superuser_required: bool = False) -> AccessToken:
        user = await self.user_repository.get(email=email)
        if not user:
            raise UserNotFoundError(f"нет пользователя с email адресом {email}")

        if superuser_required and not user.is_superuser:
            raise AccessDeniedError("Пользователь не является админом")

        if not self.password_hasher.verify(password, user.hash_password):
            raise InvalidPasswordError("Неверный пароль")

        access_token = self.jwt_processor.create_access_token(user.email, user.id)
        return access_token
