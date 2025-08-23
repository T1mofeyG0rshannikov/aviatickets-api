from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class CreatePassengerRequest(BaseModel):
    first_name: str
    second_name: str

    gender: str
    birth_date: datetime
    passport: str
    expiration_date: datetime


class CreateUserTicketRequest(BaseModel):
    ticket_id: UUID
    passangers: list[CreatePassengerRequest]


class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str
    second_name: str


class LoginRequest(BaseModel):
    email: str
    password: str
