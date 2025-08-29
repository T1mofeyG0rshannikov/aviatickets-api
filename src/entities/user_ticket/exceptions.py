from src.entities.exceptions import InvalidCredentialsError, RecordNotFoundError


class UserTicketNotFoundError(RecordNotFoundError):
    pass


class ExpiredInternationalPassportError(InvalidCredentialsError):
    pass


class InvalidInternationalPassportError(InvalidCredentialsError):
    pass
