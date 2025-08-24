import re
from dataclasses import dataclass

from src.entities.airport.exception import InvalidAirportNameError


@dataclass(frozen=True)
class AirportName:
    """
    Value Object for airport name
    """

    value: str

    def validation(self, value: str):
        pattern = re.compile(r"^[A-Za-z\s.,:;() -/\d“”’]+$")
        return bool(pattern.fullmatch(value))

    def __post_init__(self):
        if not self.validation(self.value):
            raise InvalidAirportNameError(f"{self.value} is not valid airline name")
