from src.application.auth.access_token import AccessToken
from src.application.auth.jwt_processor import JwtProcessorInterface
from src.application.dto.user import RegisterUserDTO
from src.application.usecases.user.create import CreateUser


class Register:
    def __init__(self, create_user: CreateUser, jwt_processor: JwtProcessorInterface) -> None:
        self.create_user = create_user
        self.jwt_processor = jwt_processor

    async def __call__(self, data: RegisterUserDTO) -> AccessToken:
        user = await self.create_user(
            password=data.password,
            email=data.email,
            first_name=data.first_name,
            second_name=data.second_name,
            is_superuser=data.is_superuser,
            birth_date=data.birth_date,
        )

        access_token = self.jwt_processor.create_access_token(user.email, user.id)
        return access_token
