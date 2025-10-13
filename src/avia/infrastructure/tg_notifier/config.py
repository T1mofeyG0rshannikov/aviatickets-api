from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class TelegramSenderConfig(BaseSettings):
    token: str = Field(alias="TG_BOT_TOKEN")
    users_raw_string: str = Field(alias="TG_BOT_USERS")

    @property
    def users(self) -> list[int]:
        return [int(user) for user in self.users_raw_string.split(",")]

    class Config:
        extra = "allow"
        env_file = ".env"
