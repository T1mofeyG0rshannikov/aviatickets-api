from abc import ABC, abstractmethod

from src.entities.user.value_objects.password import Password


class PasswordHasherInterface(ABC):
    @abstractmethod
    def hash_password(self, password: Password) -> str:
        ...

    @abstractmethod
    def verify(self, password: Password, hashed_password: str) -> bool:
        ...
