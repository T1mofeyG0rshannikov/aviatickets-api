class InternationalPassport(str):
    """Value Object для номера загран паспорта пассажира"""

    def __new__(cls, value):
        if not cls.is_valid(value):
            raise ValueError(f"'{value}' is not a valid international passport number.")
        return super().__new__(cls, value)

    @staticmethod
    def is_valid(value):
        return isinstance(value, str) and len(value) == 9 and all(s.isdigit() for s in value)
