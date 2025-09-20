from avia.entities.user.exceptions import InvalidPasswordError


class Password(str):
    """Value Object for user password"""

    def __new__(cls, value):
        if not cls.validate(value):
            raise InvalidPasswordError("Password is too short: minimum 6 symbols")

        return super().__new__(cls, value)

    @staticmethod
    def validate(value: str):
        return len(value) >= 6
