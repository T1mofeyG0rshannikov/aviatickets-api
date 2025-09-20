from pydantic import Field
from pydantic_settings import BaseSettings


class ExchangeRateServiceConfig(BaseSettings):
    url: str = Field(alias="CURRENCY_URL")

    class Config:
        extra = "allow"
        env_file = ".env"
