from src.entities.exceptions import (
    AccessDeniedError,
    InvalidCreditnailsError,
    RecordNotFoundException,
)


class AdminRequiredError(AccessDeniedError):
    pass


class UserRequiredError(AccessDeniedError):
    pass


class UserNotFoundError(RecordNotFoundException):
    pass


class InvalidPasswordError(AccessDeniedError):
    pass


class UserWithEmailAlreadyExistError(InvalidCreditnailsError):
    pass


class InvalidEmailError(InvalidCreditnailsError):
    pass
