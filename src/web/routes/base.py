from collections.abc import Callable
from functools import wraps

from fastapi import Depends
from starlette.requests import Request

from src.depends.depends import get_jwt_processor, get_user_repository
from src.entities.exceptions import NotPermittedError
from src.entities.user import User
from src.repositories.user_repository import UserRepository
from src.user.auth.jwt_processor import JwtProcessor


def admin_required(func: Callable = None) -> Callable:
    def wrapper(func: Callable):
        @wraps(func)
        async def wrapped_func(*args, user: User, **kwargs):
            if user and not user.is_superuser or not user:
                raise NotPermittedError("у вас нет прав для выполнения запроса")
            return await func(*args, user=user, **kwargs)

        return wrapped_func

    if func:
        return wrapper(func)
    return wrapper


async def get_user(
    request: Request,
    jwt_processor: JwtProcessor = Depends(get_jwt_processor),
    user_repository: UserRepository = Depends(get_user_repository),
) -> User:
    token = request.session.get("token")
    if token:
        payload = jwt_processor.validate_token(token)
        if payload:
            return await user_repository.get(payload["sub"])

    return None
