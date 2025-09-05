from abc import ABC, abstractmethod

from src.application.auth.access_token import AccessToken
from src.entities.user.value_objects.email import Email
from src.entities.value_objects.entity_id import EntityId


class JwtProcessorInterface(ABC):
    @abstractmethod
    def create_access_token(self, email: Email, user_id: EntityId) -> AccessToken:
        ...

    @abstractmethod
    def validate_token(self, token: str) -> dict | None:
        ...
