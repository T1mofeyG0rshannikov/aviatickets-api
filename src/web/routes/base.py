from collections.abc import Callable
from functools import wraps
from typing import Annotated

from fastapi import Depends
from starlette.requests import Request

from src.depends.annotations.annotations import UserRepositoryAnnotation
from src.depends.depends import get_jwt_processor
from src.entities.user.exceptions import AdminRequiredError, UserRequiredError
from src.entities.user.user import User
from src.infrastructure.jwt.jwt_processor import JwtProcessor


def admin_required(func: Callable = None) -> Callable:
    def wrapper(func: Callable):
        @wraps(func)
        async def wrapped_func(*args, user: User, **kwargs):
            if user and not user.is_superuser or not user:
                raise AdminRequiredError("у вас нет прав для выполнения запроса")
            return await func(*args, user=user, **kwargs)

        return wrapped_func

    if func:
        return wrapper(func)
    return wrapper


def user_required(func: Callable = None) -> Callable:
    def wrapper(func: Callable):
        @wraps(func)
        async def wrapped_func(*args, user: User, **kwargs):
            if not user:
                raise UserRequiredError("Войдите в аккаунт для выполнения действия")
            return await func(*args, user=user, **kwargs)

        return wrapped_func

    if func:
        return wrapper(func)
    return wrapper


async def get_user(
    request: Request,
    user_repository: UserRepositoryAnnotation,
    jwt_processor: Annotated[JwtProcessor, Depends(get_jwt_processor)],
) -> User:
    token = request.session.get("token")
    if token:
        payload = jwt_processor.validate_token(token)
        if payload:
            return await user_repository.get(payload["sub"])

    return None
