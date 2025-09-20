from pydantic import Field
from pydantic_settings import BaseSettings


class AdminConfig(BaseSettings):
    secret_key: str = Field(alias="ADMIN_SECRET_KEY")

    class Config:
        extra = "allow"
        env_file = ".env"
