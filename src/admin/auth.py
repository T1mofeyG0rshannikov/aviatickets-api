from typing import Annotated, Self

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from src.admin.config import AdminConfig
from src.depends.base import get_login_interactor
from src.depends.decorator import inject_dependencies
from src.entities.exceptions import AccessDeniedError
from src.entities.user.exceptions import InvalidPasswordError, UserNotFoundError
from src.infrastructure.jwt.jwt_processor import JwtProcessor
from src.infrastructure.security.password_hasher import PasswordHasher
from src.usecases.user.login import Login
from src.web.schemas.login import LoginResponse


class AdminAuth(AuthenticationBackend):
    def __init__(self, password_hasher: PasswordHasher, config: AdminConfig, jwt_processor: JwtProcessor) -> None:
        super().__init__(config.admin_secret_key)
        self.password_hasher = password_hasher
        self.jwt_processor = jwt_processor
        self.config = config

    @inject_dependencies
    async def login(self: Self, request: Request, login: Annotated[Login, get_login_interactor]) -> LoginResponse:
        if self.config.debug:
            LoginResponse(ok=True)

        form = await request.form()
        email, password = form["email"], form["password"]

        try:
            access_token = await login(email, password)
            request.session.update({"token": access_token})
            return LoginResponse(ok=True)
        except (UserNotFoundError, InvalidPasswordError) as e:
            return LoginResponse(ok=False, email_error_message=str(e))
        except AccessDeniedError:
            return LoginResponse(ok=False, email_error_message="Недостаточно прав для входа в панель администратора")

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        if self.config.debug:
            return True

        token = request.session.get("token")

        if token and self.jwt_processor.validate_token(token):
            return True

        return False
