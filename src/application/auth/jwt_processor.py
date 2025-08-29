from abc import ABC, abstractmethod
from uuid import UUID

from src.application.auth.access_token import AccessToken


class JwtProcessorInterface(ABC):
    @abstractmethod
    def create_access_token(self, email: str, user_id: UUID) -> AccessToken:
        ...

    @abstractmethod
    def validate_token(self, token: str) -> dict | None:
        ...
