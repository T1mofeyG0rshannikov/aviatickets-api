from pydantic import Field
from pydantic_settings import BaseSettings


class AmadeusAPIConfig(BaseSettings):
    oauth2_url: str = Field(alias="AMADEUS_API_OAUTH_URL")
    secret: str = Field(alias="AMADEUS_API_SECRET")
    api_key: str = Field(alias="AMADEUS_API_KEY")
    url: str = Field(alias="AMADEUS_API_URL")

    class Config:
        env_file = ".env"
        extra = "allow"
