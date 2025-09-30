from dataclasses import dataclass
from enum import StrEnum

from avia.entities.aircraft.exceptions import InvalidAircraftIATACodeError


class AircraftWTCEnum(StrEnum):
    l = "light"
    m = "medium"
    h = "heavy"
    j = "super"


@dataclass(frozen=True)
class AircraftWTC:
    """Value Object for aircraft wtc"""

    value: AircraftWTCEnum

    def __pre_save__(self):
        if not self.is_valid(self.value):
            raise InvalidAircraftIATACodeError(f"'{self.value}' is not a valid WTC for aircraft.")

    @classmethod
    def is_valid(cls, value):
        return isinstance(value, str) and value in [v.value for v in AircraftWTCEnum]
