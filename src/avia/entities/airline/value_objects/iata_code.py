from dataclasses import dataclass

from avia.entities.airline.exceptions import InvalidAirlineIATACodeError


@dataclass(frozen=True)
class IATACode(str):
    """Value Object for airline IATA code"""

    value: str

    def __pre_save__(self):
        if not self.is_valid_iata(self.value):
            raise InvalidAirlineIATACodeError(f"'{self.value}' is not a valid IATA code for airline.")

    @staticmethod
    def valid_letter(letter: str) -> bool:
        return (letter.isalpha() and letter.isupper()) or letter.isdigit()

    @staticmethod
    def is_valid_iata(value):
        return isinstance(value, str) and len(value) == 2 and all(IATACode.valid_letter(letter) for letter in value)
