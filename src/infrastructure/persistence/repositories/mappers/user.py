from src.entities.user.user import User
from src.entities.user.value_objects.email import Email
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import UserOrm


def from_orm_to_user(user: UserOrm) -> User:
    return User(
        id=EntityId(user.id),
        first_name=user.first_name,
        second_name=user.second_name,
        email=Email(user.email),
        hash_password=user.hash_password,
        is_superuser=user.is_superuser,
        is_active=user.is_active,
    )
