class RecordNotFoundException(Exception):
    pass


class AirportNotFoundException(RecordNotFoundException):
    pass


class FetchAPIException(Exception):
    pass


class NotPermittedError(Exception):
    pass
