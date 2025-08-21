class RecordNotFoundError(Exception):
    pass


class AirportNotFoundError(RecordNotFoundError):
    pass


class FetchAPIError(Exception):
    pass


class AccessDeniedError(Exception):
    pass


class InvalidcredentialsError(Exception):
    pass


class InvalidParseParamsError(InvalidcredentialsError):
    pass
