from src.entities.user.user import User
from src.entities.user.value_objects.email import Email
from src.entities.user.value_objects.first_name import FirstName
from src.entities.user.value_objects.second_name import SecondName


class UserFactory:
    @classmethod
    def create(
        cls,
        first_name: str,
        second_name: str,
        email: str,
        hash_password: str,
        is_superuser: bool = False,
        is_active: bool = True,
    ) -> User:
        return User.create(
            first_name=FirstName(first_name),
            second_name=SecondName(second_name),
            email=Email(email),
            hash_password=hash_password,
            is_superuser=is_superuser,
            is_active=is_active,
        )
