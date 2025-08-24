from src.entities.exceptions import DomainError, RecordNotFoundError


class TicketNotFoundError(RecordNotFoundError):
    pass


class DepartureAtInPastError(DomainError):
    pass


class ReturnAtInPastError(DomainError):
    pass


class DepartureAtMustBeBeforeReturnAtError(DomainError):
    pass


class InvalidFlightNumberError(DomainError):
    pass
