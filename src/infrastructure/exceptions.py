from src.entities.exceptions import InvalidcredentialsError


class FetchAPIError(Exception):
    pass


class InvalidParseParamsError(InvalidcredentialsError):
    pass
