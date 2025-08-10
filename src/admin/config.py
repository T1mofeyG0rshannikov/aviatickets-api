from pydantic_settings import BaseSettings


class AdminConfig(BaseSettings):
    admin_secret_key: str
    debug: bool

    class Config:
        extra = "allow"
        env_file = ".env"
