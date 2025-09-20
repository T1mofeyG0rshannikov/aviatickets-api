class RecordNotFoundError(Exception):
    pass


class AirportNotFoundError(RecordNotFoundError):
    pass


class AccessDeniedError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class DomainError(Exception):
    pass
