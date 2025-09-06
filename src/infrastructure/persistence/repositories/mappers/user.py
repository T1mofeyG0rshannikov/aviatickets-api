from src.entities.user.user import User
from src.entities.user.value_objects.email import Email
from src.entities.user.value_objects.first_name import FirstName
from src.entities.user.value_objects.second_name import SecondName
from src.entities.user.value_objects.user_id import UserId
from src.infrastructure.persistence.db.models.models import UserOrm


def from_orm_to_user(user: UserOrm) -> User:
    return User(
        id=UserId(value=user.id),
        first_name=FirstName(user.first_name),
        second_name=SecondName(user.second_name),
        email=Email(user.email),
        hash_password=user.hash_password,
        is_superuser=user.is_superuser,
        is_active=user.is_active,
    )
