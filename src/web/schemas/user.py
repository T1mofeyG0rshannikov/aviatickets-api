from typing import List

from pydantic import BaseModel

from src.entities.user_ticket.dto import CreatePassengerDTO


class CreateUserTicketRequest(BaseModel):
    ticket_id: int
    passangers: list[CreatePassengerDTO]


class RegisterRequest(BaseModel):
    email: str
    password: str
    first_name: str
    second_name: str


class LoginRequest(BaseModel):
    email: str
    password: str
