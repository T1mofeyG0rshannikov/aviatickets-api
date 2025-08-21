from pydantic import Field
from pydantic_settings import BaseSettings


class AviasalesAPIConfig(BaseSettings):
    api_token: str = Field(alias="AVIASALES_API_KEY")
    url: str = Field(alias="AVIASALES_API_URL")

    class Config:
        env_file = ".env"
        extra = "allow"
