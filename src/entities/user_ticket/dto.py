from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreatePassengerDTO:
    first_name: str
    second_name: str

    gender: str
    birth_date: datetime
