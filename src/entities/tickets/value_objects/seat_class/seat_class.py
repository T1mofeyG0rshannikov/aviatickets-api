from dataclasses import dataclass

from src.entities.tickets.value_objects.seat_class.enum import SeatClassEnum
from src.entities.tickets.exceptions import InvalidSeatClassError


@dataclass(frozen=True)
class SeatClass:
    value: str

    CLASSES = [
        seat.value for seat in SeatClassEnum
    ]

    def __post_init__(self):
        if self.value not in self.CLASSES:
            raise InvalidSeatClassError(f'''"{self.value}" is invalid seat class. Choices is {", ".join(map(lambda f: f'"{f}"', self.CLASSES))}''')