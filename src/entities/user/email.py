import re


class Email(str):
    """Value Object для email пользователя"""

    def __new__(cls, value):
        if not cls.is_valid_email(value):
            raise ValueError(f"'{value}' is not a valid Email.")
        return super().__new__(cls, value)

    @staticmethod
    def is_valid_email(value):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, value))
