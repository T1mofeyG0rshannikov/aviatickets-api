from pydantic import Field
from pydantic_settings import BaseSettings


class PdfGeneratorConfig(BaseSettings):
    pdf_tickets_folder: str = Field(alias="PDF_TICKETS_FOLDER")

    class Config:
        extra = "allow"
        env_file = ".env"
