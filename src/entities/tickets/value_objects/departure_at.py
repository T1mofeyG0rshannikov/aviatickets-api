from dataclasses import dataclass
from datetime import datetime

from src.entities.tickets.exceptions import DepartureAtInPastError


@dataclass(frozen=True)
class DepartureAt:
    """
    Value Object for ticket departure at
    """

    value: datetime

    def validation(self, value: datetime):
        if value < datetime.now():
            raise DepartureAtInPastError("departure at cant be in the past")

    def __post_init__(self):
        self.validation(self.value)

    def __str__(self):
        return self.value.isoformat()

    def __lt__(self, other):
        if not isinstance(other, DepartureAt):
            return NotImplemented
        return self.value < other.value

    def __gt__(self, other):
        if not isinstance(other, DepartureAt):
            return NotImplemented
        return self.value > other.value

    def __eq__(self, other):
        if not isinstance(other, DepartureAt):
            return NotImplemented
        return self.value == other.value
