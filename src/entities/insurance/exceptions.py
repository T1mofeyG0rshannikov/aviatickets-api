from src.entities.exceptions import DomainError, RecordNotFoundError


class InsuranceNotFoundError(RecordNotFoundError):
    pass


class InsuranceAlreadyExistError(DomainError):
    pass
