from src.entities.exceptions import DomainError


class InvalidAirlineIATACodeError(DomainError):
    pass


class InvalidAirlineICAOCodeError(DomainError):
    pass


class InvalidAirlineNameError(DomainError):
    pass


class InvalidAirlineNameRussianError(DomainError):
    pass
