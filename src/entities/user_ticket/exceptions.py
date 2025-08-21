from src.entities.exceptions import InvalidcredentialsError, RecordNotFoundError


class UserTicketNotFoundError(RecordNotFoundError):
    pass


class ExpiredInternationalPassportError(InvalidcredentialsError):
    pass
