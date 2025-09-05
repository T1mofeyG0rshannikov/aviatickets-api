from dataclasses import dataclass
from datetime import datetime

from src.entities.tickets.exceptions import DepartureAtInPastError


@dataclass(frozen=True)
class DepartureAt:
    """
    Value Object for ticket departure at in local timezone
    """

    value: datetime

    def validation(self, value: datetime):
        if value < datetime.now(value.tzinfo):
            raise DepartureAtInPastError("departure at cant be in the past")

    def __post_init__(self):
        self.validation(self.value)

    def __str__(self):
        return self.value.isoformat()
