from datetime import datetime, timedelta

from jose import JWTError, jwt

from src.user.auth.jwt_config import JwtConfig


class JwtProcessor:
    def __init__(self, jwt_settings: JwtConfig) -> None:
        self.jwt_settings = jwt_settings

    def create_access_token(self, email: str, user_id: int) -> str:
        encode = {"sub": email, "id": user_id}
        expires = datetime.utcnow() + timedelta(hours=self.jwt_settings.expires_in)
        encode.update({"exp": expires})
        return jwt.encode(encode, self.jwt_settings.secret_key, algorithm=self.jwt_settings.algorithm)

    def validate_token(self, token: str) -> dict | None:
        try:
            payload = jwt.decode(token, self.jwt_settings.secret_key, algorithms=[self.jwt_settings.algorithm])
            return payload
        except JWTError:
            return None
