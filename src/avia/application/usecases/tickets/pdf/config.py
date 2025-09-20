from pydantic import Field
from pydantic_settings import BaseSettings


class PdfGeneratorConfig(BaseSettings):
    pdf_tickets_folder: str = Field(alias="PDF_TICKETS_FOLDER")
    pdf_insurance_folder: str = Field(alias="PDF_INSURANCES_FOLDER")
    pdf_insurance_template_path: str = Field(alias="PDF_INSURANCES_TEMPLATE_PATH")

    class Config:
        extra = "allow"
        env_file = ".env"
