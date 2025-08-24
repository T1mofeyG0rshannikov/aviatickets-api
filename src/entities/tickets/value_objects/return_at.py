from dataclasses import dataclass
from datetime import datetime

from src.entities.tickets.exceptions import ReturnAtInPastError


@dataclass(frozen=True)
class ReturnAt:
    """
    Value Object for ticket return at in local timezone
    """

    value: datetime

    def validation(self, value: datetime):
        print(value, datetime.now(), value.tzinfo)
        if value < datetime.now(value.tzinfo):
            raise ReturnAtInPastError("return at cant be in the past")

    def __post_init__(self):
        self.validation(self.value)

    def __str__(self):
        return self.value.isoformat()
