from pydantic_settings import BaseSettings


class EmailSenderConfig(BaseSettings):
    sender_email: str
    sender_password: str

    class Config:
        env_file = ".env"
        extra = "allow"
