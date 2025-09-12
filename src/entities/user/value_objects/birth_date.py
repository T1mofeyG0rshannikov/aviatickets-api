from dataclasses import dataclass
from datetime import date, datetime

from src.entities.user.exceptions import BirthDateInFutureErro


@dataclass(frozen=True)
class BirthDate:
    """
    Value Object for users birth date
    """

    value: date

    def __pre_save__(self):
        if self.value > datetime.now(self.value.tzinfo):
            raise BirthDateInFutureErro("birth date cant be in the future")

    def __str__(self) -> str:
        return str(self.value)
