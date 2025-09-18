from dataclasses import dataclass
from enum import StrEnum

from src.entities.aircraft.exceptions import InvalidAircraftIATACodeError


class AircraftWTCEnum(StrEnum):
    l = "light"  # type: ignore
    m = "medium"
    h = "heavy"
    j = "super"


@dataclass(frozen=True)
class AircraftWTC:
    """Value Object for aircraft wtc"""

    value: AircraftWTCEnum

    def __pre_save__(cls, value):
        if not cls.is_valid(value):
            raise InvalidAircraftIATACodeError(f"'{value}' is not a valid IATA code for airline.")
        return super().__new__(cls, value)

    @classmethod
    def is_valid(cls, value):
        return isinstance(value, str) and len(value) == 3 and all(cls.valid_letter(letter) for letter in value)
