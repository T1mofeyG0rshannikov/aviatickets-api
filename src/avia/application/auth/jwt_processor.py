from abc import ABC, abstractmethod

from avia.application.auth.access_token import AccessToken
from avia.entities.user.value_objects.email import Email
from avia.entities.user.value_objects.user_id import UserId


class JwtProcessorInterface(ABC):
    @abstractmethod
    def create_access_token(self, email: Email, user_id: UserId) -> AccessToken:
        ...

    @abstractmethod
    def validate_token(self, token: str) -> dict | None:
        ...
