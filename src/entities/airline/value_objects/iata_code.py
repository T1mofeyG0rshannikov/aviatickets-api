from src.entities.airline.exceptions import InvalidAirlineIATACodeError


class IATACode(str):
    """Value Object for airline IATA code"""

    def __new__(cls, value):
        if not cls.is_valid_iata(value):
            raise InvalidAirlineIATACodeError(f"'{value}' is not a valid IATA code for airline.")
        return super().__new__(cls, value)

    @staticmethod
    def valid_letter(letter: str) -> bool:
        return (letter.isalpha() and letter.isupper()) or letter.isdigit()

    @classmethod
    def is_valid_iata(cls, value):
        return isinstance(value, str) and len(value) == 2 and all(cls.valid_letter(letter) for letter in value)
