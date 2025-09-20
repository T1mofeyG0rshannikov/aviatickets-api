from dataclasses import dataclass

from avia.entities.aircraft.exceptions import InvalidAircraftIATACodeError


@dataclass(frozen=True)
class IATACode:
    """Value Object for aircraft IATA code"""

    value: str

    def __pre_save__(cls, value):
        if not cls.is_valid(value):
            raise InvalidAircraftIATACodeError(f"'{value}' is not a valid IATA code for aircraft.")
        return super().__new__(cls, value)

    @staticmethod
    def valid_letter(letter: str) -> bool:
        return (letter.isalpha() and letter.isupper()) or letter.isdigit()

    @classmethod
    def is_valid(cls, value):
        return isinstance(value, str) and len(value) == 3 and all(cls.valid_letter(letter) for letter in value)
