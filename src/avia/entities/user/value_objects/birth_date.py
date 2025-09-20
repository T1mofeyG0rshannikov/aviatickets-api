from dataclasses import dataclass
from datetime import date, datetime

from avia.entities.user.exceptions import BirthDateInFutureErro


@dataclass(frozen=True)
class BirthDate:
    """
    Value Object for users birth date
    """

    value: date

    @staticmethod
    def validate(value: date) -> bool:
        return value <= datetime.now().date()

    def __pre_save__(self):
        if not BirthDate.validate(self.value):
            raise BirthDateInFutureErro("birth date cant be in the future")

    def __str__(self) -> str:
        return str(self.value)
