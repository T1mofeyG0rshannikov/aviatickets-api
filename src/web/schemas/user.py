from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel


class CreatePassengerRequest(BaseModel):
    first_name: str
    second_name: str

    gender: str
    birth_date: datetime
    passport: str
    expiration_date: date


class CreateUserTicketRequest(BaseModel):
    ticket_id: UUID
    passengers: list[CreatePassengerRequest]


class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str
    second_name: str


class LoginRequest(BaseModel):
    email: str
    password: str
