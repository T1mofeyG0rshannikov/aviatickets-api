from src.entities.exceptions import InvalidCredentialsError


class FetchAPIError(Exception):
    pass


class InvalidParseParamsError(InvalidCredentialsError):
    pass


class InvalidFileContentException(Exception):
    pass
