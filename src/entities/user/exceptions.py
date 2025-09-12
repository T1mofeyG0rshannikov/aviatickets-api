from src.entities.exceptions import (
    AccessDeniedError,
    DomainError,
    InvalidCredentialsError,
    RecordNotFoundError,
)


class AdminRequiredError(AccessDeniedError):
    pass


class UserRequiredError(AccessDeniedError):
    pass


class UserNotFoundError(RecordNotFoundError):
    pass


class InvalidPasswordError(AccessDeniedError):
    pass


class UserWithEmailAlreadyExistError(InvalidCredentialsError):
    pass


class InvalidEmailError(DomainError):
    pass


class InvalidFirstNameError(DomainError):
    pass


class InvalidSecondNameError(DomainError):
    pass


class BirthDateInFutureErro(DomainError):
    pass
