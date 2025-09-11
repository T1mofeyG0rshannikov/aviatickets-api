import re
from dataclasses import dataclass

from src.entities.user.exceptions import InvalidSecondNameError


@dataclass(frozen=True)
class SecondName:
    """
    Value Object for users second name
    """

    value: str

    def validation(self, value: str):
        pattern = re.compile(r"^[А-Яa-яЁё]+$")
        return bool(pattern.fullmatch(value))

    def __pre_save__(self):
        if not self.validation(self.value):
            raise InvalidSecondNameError(f"{self.value} is not valid user second name")
        self.value = self.value.capitalize()

    def __str__(self) -> str:
        return self.value
