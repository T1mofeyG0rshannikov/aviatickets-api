from passlib.context import CryptContext

from src.application.auth.password_hasher import PasswordHasherInterface
from src.entities.user.value_objects.password import Password


class PasswordHasher(PasswordHasherInterface):
    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: Password) -> str:
        return self.pwd_context.hash(password)

    def verify(self, password: Password, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)
