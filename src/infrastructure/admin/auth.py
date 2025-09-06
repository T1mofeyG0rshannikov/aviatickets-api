from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.entities.exceptions import AccessDeniedError
from src.entities.user.exceptions import InvalidPasswordError, UserNotFoundError
from src.infrastructure.admin.config import AdminConfig
from src.infrastructure.admin.login_response import AdminLoginResponse
from src.infrastructure.factories.login import LoginFactoryInterface
from src.infrastructure.jwt.jwt_processor import JwtProcessor
from src.infrastructure.security.password_hasher import PasswordHasher


class AdminAuth(AuthenticationBackend):
    def __init__(
        self,
        password_hasher: PasswordHasher,
        config: AdminConfig,
        jwt_processor: JwtProcessor,
        login_factory: LoginFactoryInterface,
    ) -> None:
        super().__init__(config.secret_key)
        self.password_hasher = password_hasher
        self.jwt_processor = jwt_processor
        self.config = config
        self.login_factory = login_factory

    async def login(self, request: Request) -> AdminLoginResponse:
        login = await self.login_factory.get_login()

        form = await request.form()
        email, password = form["email"], form["password"]

        try:
            access_token = await login(email, password)
            request.session.update({"token": access_token})
            return AdminLoginResponse(ok=True)
        except (UserNotFoundError, InvalidPasswordError) as e:
            return AdminLoginResponse(ok=False, email_error_message=str(e))
        except AccessDeniedError:
            return AdminLoginResponse(
                ok=False, email_error_message="Недостаточно прав для входа в панель администратора"
            )

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if token and self.jwt_processor.validate_token(token):
            return True

        return False
