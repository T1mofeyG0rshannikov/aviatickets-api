from src.entities.exceptions import InvalidCredentialsError


class InvalidParseParamsError(InvalidCredentialsError):
    pass


class InvalidFileContentException(Exception):
    pass
