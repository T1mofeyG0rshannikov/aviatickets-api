import re
from dataclasses import dataclass

from src.entities.tickets.exceptions import InvalidFlightNumberError


@dataclass(frozen=True)
class FlightNumber:
    """
    Value Object for ticket departure at
    """

    value: str

    def validation(self, value: str):
        pattern = r"^[A-Z]{2}\-\d{1,4}[A-Z]?$"
        return bool(re.match(pattern, value))

    def __post_init__(self):
        if not self.validation(self.value):
            raise InvalidFlightNumberError(f"{self.value} is not valid flight number")
