from src.application.auth.password_hasher import PasswordHasherInterface
from src.application.factories.user_factory import UserFactory
from src.entities.user.exceptions import UserWithEmailAlreadyExistError
from src.entities.user.user import User
from src.entities.user.user_repository import UserRepositoryInterface
from src.entities.user.value_objects.password import Password


class CreateUser:
    def __init__(self, user_repository: UserRepositoryInterface, password_hasher: PasswordHasherInterface) -> None:
        self.repository = user_repository
        self.password_hasher = password_hasher

    async def __call__(
        self, password: str, email: str, first_name: str, second_name: str, is_superuser: bool = False
    ) -> User:
        password = Password(password)

        hashed_password = self.password_hasher.hash_password(password)

        user_by_email = await self.repository.get(email=email)
        if user_by_email is not None:
            raise UserWithEmailAlreadyExistError(f"User with email '{email}' already exist")

        user = UserFactory.create(
            email=email,
            first_name=first_name,
            second_name=second_name,
            hash_password=hashed_password,
            is_superuser=is_superuser,
        )

        await self.repository.save(user)
        return user
