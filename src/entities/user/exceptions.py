from src.entities.exceptions import (
    AccessDeniedError,
    InvalidcredentialsError,
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


class UserWithEmailAlreadyExistError(InvalidcredentialsError):
    pass


class InvalidEmailError(InvalidcredentialsError):
    pass
