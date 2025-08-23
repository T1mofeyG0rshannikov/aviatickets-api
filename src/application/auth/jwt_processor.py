from abc import ABC, abstractmethod

from src.application.auth.access_token import AccessToken


class JwtProcessorInterface(ABC):
    @abstractmethod
    def create_access_token(self, email: str, user_id: int) -> AccessToken:
        ...

    @abstractmethod
    def validate_token(self, token: str) -> dict | None:
        ...
