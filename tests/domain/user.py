import pytest

from src.entities.user.exceptions import InvalidEmailError
from src.entities.user.user import User
from src.entities.user.value_objects.email import Email


@pytest.mark
def test_create_user():
    user = User.create(
        first_name="Тимофей", second_name="Марков", email=Email("timofey@mail.ru"), hash_password="hash_password"
    )

    assert isinstance(user, User)


@pytest.mark
def test_create_user_with_empty_name():
    with pytest.raises(ValueError) as excinfo:
        User.create(first_name="", second_name="Марков", email=Email("timofey@mail.ru"), hash_password="hash_password")

    assert "first_name is required" in str(excinfo.value)


@pytest.mark
def test_create_user_with_invalid_email():
    invalid_email = "8988929983"

    with pytest.raises(InvalidEmailError) as excinfo:
        User.create(
            first_name="Тимофей", second_name="Марков", email=Email(invalid_email), hash_password="hash_password"
        )

    assert f"'{invalid_email}' is not a valid Email." in str(excinfo.value)
