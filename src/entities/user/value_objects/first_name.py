import re
from dataclasses import dataclass

from src.entities.user.exceptions import InvalidFirstNameError


@dataclass(frozen=True)
class FirstName:
    """
    Value Object for users first name
    """

    value: str

    def validation(self, value: str):
        pattern = re.compile(r"^[А-Яa-яЁё]+$")
        return bool(pattern.fullmatch(value))

    def __pre_save__(self):
        if not self.validation(self.value):
            raise InvalidFirstNameError(f"{self.value} is not valid user first name")
        self.value = self.value.capitalize()

    def __str__(self) -> str:
        return self.value
