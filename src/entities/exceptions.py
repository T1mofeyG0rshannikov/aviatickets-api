class RecordNotFoundException(Exception):
    pass


class AirportNotFoundException(RecordNotFoundException):
    pass


class FetchAPIException(Exception):
    pass


class AccessDeniedError(Exception):
    pass


class InvalidCreditnailsError(Exception):
    pass
