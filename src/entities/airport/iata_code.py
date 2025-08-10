class IATACode(str):
    """Value Object для IATA кода"""

    def __new__(cls, value):
        if not cls.is_valid_iata(value):
            raise ValueError(f"'{value}' is not a valid IATA code.")
        return super().__new__(cls, value)

    @staticmethod
    def is_valid_iata(value):
        return isinstance(value, str) and len(value) == 3 and value.isalpha() and value.isupper()
