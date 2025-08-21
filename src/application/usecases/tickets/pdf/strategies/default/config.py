from pydantic import Field
from pydantic_settings import BaseSettings


class DefaultPdfTicketAdapterConfig(BaseSettings):
    nav_path: str = Field(alias="NAV_PDF_PATH")
    single_ticket_path: str = Field(alias="SINGLE_TICKET_PDF_PATH")
    bottom_path: str = Field(alias="BOTTOM_PDF_PATH")

    class Config:
        extra = "allow"
        env_file = ".env"
