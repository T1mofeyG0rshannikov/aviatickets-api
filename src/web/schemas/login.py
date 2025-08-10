from pydantic import BaseModel


class LoginResponse(BaseModel):
    ok: bool
    email_error_message: str | None = None
    password_error_message: str | None = None
