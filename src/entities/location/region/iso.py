import re


class ISOCode(str):
    """Value Object для ISO кода региона"""

    def __new__(cls, value):
        if not cls.is_valid_iata(value):
            raise ValueError(f"'{value}' is not a valid ISO code.")
        return super().__new__(cls, value)

    @staticmethod
    def is_valid_iata(value):
        regex = r"^[A-Z]{2}-[A-Z0-9]{2,3}$"
        return isinstance(value, str) and (re.match(regex, value) is not None)
