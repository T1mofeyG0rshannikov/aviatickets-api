class ICAOCode(str):
    """Value Object для ICAO кода аэропорта"""

    def __new__(cls, value):
        if not cls.is_valid_iata(value):
            raise ValueError(f"'{value}' is not a valid ICAO code for airline.")
        return super().__new__(cls, value)

    @staticmethod
    def is_valid_iata(value):
        return isinstance(value, str) and len(value) == 3 and value.isalpha() and value.isupper()
