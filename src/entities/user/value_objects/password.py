from src.entities.user.exceptions import InvalidPasswordError


class Password(str):
    """Value Object for user password"""

    def __new__(cls, value):
        cls.validate(value)
        return super().__new__(cls, value)

    @staticmethod
    def validate(value: str):
        if len(value) < 6:
            raise InvalidPasswordError("Password is too short: minimum 6 symbols")

        return True
