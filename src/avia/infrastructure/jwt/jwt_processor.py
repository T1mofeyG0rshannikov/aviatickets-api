from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt

from avia.application.auth.access_token import AccessToken
from avia.application.auth.jwt_processor import JwtProcessorInterface
from avia.entities.user.value_objects.email import Email
from avia.entities.user.value_objects.user_id import UserId
from avia.infrastructure.jwt.jwt_config import JwtConfig


class JwtProcessor(JwtProcessorInterface):
    def __init__(self, jwt_settings: JwtConfig) -> None:
        self.jwt_settings = jwt_settings

    def create_access_token(self, email: Email, user_id: UserId) -> AccessToken:
        encode: dict[str, Any] = {"sub": email, "id": str(user_id)}
        expires = datetime.utcnow() + timedelta(hours=self.jwt_settings.expires_in)
        encode.update({"exp": expires})
        return AccessToken(jwt.encode(encode, self.jwt_settings.secret_key, algorithm=self.jwt_settings.algorithm))

    def validate_token(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(token, self.jwt_settings.secret_key, algorithms=[self.jwt_settings.algorithm])
            return payload
        except JWTError:
            return None
