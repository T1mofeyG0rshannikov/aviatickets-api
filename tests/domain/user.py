import pytest

from src.application.factories.user_factory import UserFactory
from src.entities.user.exceptions import InvalidEmailError
from src.entities.user.user import User


@pytest.mark
def test_create_user():
    user = UserFactory.create(
        first_name="Тимофей", second_name="Марков", email="timofey@mail.ru", hash_password="hash_password"
    )

    assert isinstance(user, User)


@pytest.mark
def test_create_user_with_empty_name():
    with pytest.raises(ValueError) as excinfo:
        UserFactory.create(first_name="", second_name="Марков", email="timofey@mail.ru", hash_password="hash_password")

    assert "first_name is required" in str(excinfo.value)


@pytest.mark
def test_create_user_with_invalid_email():
    invalid_email = "8988929983"

    with pytest.raises(InvalidEmailError) as excinfo:
        UserFactory.create(
            first_name="Тимофей", second_name="Марков", email=invalid_email, hash_password="hash_password"
        )

    assert f"'{invalid_email}' is not a valid Email." in str(excinfo.value)
