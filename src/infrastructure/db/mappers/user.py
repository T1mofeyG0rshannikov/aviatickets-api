from src.entities.user.user import User
from src.infrastructure.db.models.models import UserOrm


def from_orm_to_user(user: UserOrm) -> User:
    return User(
        id=user.id,
        first_name=user.first_name,
        second_name=user.second_name,
        email=user.email,
        hash_password=user.hash_password,
        is_superuser=user.is_superuser,
        is_active=user.is_active,
    )
