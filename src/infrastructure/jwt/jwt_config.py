from pydantic_settings import BaseSettings


class JwtConfig(BaseSettings):
    secret_key: str
    algorithm: str
    expires_in: int

    class Config:
        extra = "allow"
        env_file = ".env"
