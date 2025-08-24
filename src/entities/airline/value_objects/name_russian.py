import re
from dataclasses import dataclass

from src.entities.airline.exceptions import InvalidAirlineNameRussianError


@dataclass(frozen=True)
class AirlineNameRussian:
    """
    Value Object for airline russian name
    """

    value: str

    def validation(self, value: str):
        pattern = re.compile(r"^[А-Яа-я\s.,:;() -/\d“”’]+$")
        return bool(pattern.fullmatch(value))

    def __post_init__(self):
        if not self.validation(self.value):
            raise InvalidAirlineNameRussianError(f"{self.value} is not valid airline russian name")
