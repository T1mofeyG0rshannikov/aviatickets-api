import re
from dataclasses import dataclass

from avia.entities.user.exceptions import InvalidFirstNameError


@dataclass(frozen=True)
class FirstName:
    """
    Value Object for users first name
    """

    value: str

    @staticmethod
    def validation(value: str) -> bool:
        pattern = re.compile(r"^[А-Яa-яЁё]+$")
        return bool(pattern.fullmatch(value)) and len(value) > 0

    @classmethod
    def create(cls, value: str):
        print(value, "VALUE")
        if not cls.validation(value):
            raise InvalidFirstNameError(f"{value} is not valid user first name")

        return FirstName(value.capitalize())

    def __str__(self) -> str:
        return self.value
