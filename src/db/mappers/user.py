from src.db.models.models import UserOrm
from src.entities.user import User


def from_orm_to_user(user: UserOrm) -> User:
    return User(
        id=user.id,
        username=user.username,
        email=user.email,
        hash_password=user.hash_password,
        is_superuser=user.is_superuser,
        is_active=user.is_active,
    )
