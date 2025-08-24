from src.entities.exceptions import DomainError


class InvalidAirportIATACodeError(DomainError):
    pass


class InvalidAirportICAOCodeError(DomainError):
    pass


class InvalidAirportNameError(DomainError):
    pass


class InvalidAirportNameRussianError(DomainError):
    pass
