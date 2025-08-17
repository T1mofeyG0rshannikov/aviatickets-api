from src.entities.user.access_token import AccessToken
from src.entities.user.dto import CreateUserDTO, RegisterUserDTO
from src.entities.user.email import Email
from src.entities.user.exceptions import (
    InvalidEmailError,
    UserWithEmailAlreadyExistError,
)
from src.infrastructure.jwt.jwt_processor import JwtProcessor
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.security.password_hasher import PasswordHasher


class Register:
    def __init__(
        self, user_repository: UserRepository, jwt_processor: JwtProcessor, password_hasher: PasswordHasher
    ) -> None:
        self.user_repository = user_repository
        self.jwt_processor = jwt_processor
        self.password_hasher = password_hasher

    async def __call__(self, data: RegisterUserDTO) -> AccessToken:
        hashed_password = self.password_hasher.hash_password(data.password)

        user_by_email = await self.user_repository.get(email=data.email)
        if user_by_email is not None:
            raise UserWithEmailAlreadyExistError(f"Пользователь с почтой '{data.email}' уже существует")

        try:
            create_dto = CreateUserDTO(
                email=Email(data.email),
                first_name=data.first_name,
                second_name=data.second_name,
                hashed_password=hashed_password,
                is_superuser=False,
            )
        except ValueError as e:
            raise InvalidEmailError(str(e))

        user = await self.user_repository.create(create_dto)
        access_token = self.jwt_processor.create_access_token(user.email, user.id)
        return access_token
