from avia.application.auth.access_token import AccessToken
from avia.application.auth.jwt_processor import JwtProcessorInterface
from avia.application.auth.password_hasher import PasswordHasherInterface
from avia.entities.exceptions import AccessDeniedError
from avia.entities.user.exceptions import InvalidPasswordError, UserNotFoundError
from avia.entities.user.user_repository import UserRepositoryInterface
from avia.entities.user.value_objects.email import Email
from avia.entities.user.value_objects.password import Password


class Login:
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        jwt_processor: JwtProcessorInterface,
        password_hasher: PasswordHasherInterface,
    ) -> None:
        self.user_repository = user_repository
        self.jwt_processor = jwt_processor
        self.password_hasher = password_hasher

    async def __call__(self, email: Email, password: Password, superuser_required: bool = False) -> AccessToken:
        user = await self.user_repository.get(email=email)
        if not user:
            raise UserNotFoundError(f"нет пользователя с email адресом {email}")

        if superuser_required and not user.is_superuser:
            raise AccessDeniedError("Пользователь не является админом")

        if not self.password_hasher.verify(password, user.hash_password):
            raise InvalidPasswordError("Неверный пароль")

        access_token = self.jwt_processor.create_access_token(user.email, user.id)
        return access_token
