import re
from dataclasses import dataclass

from src.entities.airline.exceptions import InvalidAirlineNameError


@dataclass(frozen=True)
class AirlineName:
    """
    Value Object for airline name
    """

    value: str

    def validation(self, value: str):
        pattern = re.compile(r"^[A-Za-z\s.,:;() -/\d“”’]+$")
        return bool(pattern.fullmatch(value))

    def __post_init__(self):
        if not self.validation(self.value):
            raise InvalidAirlineNameError(f"{self.value} is not valid airline name")
