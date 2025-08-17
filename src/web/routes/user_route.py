from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response

from src.depends.annotations.user_annotation import UserAnnotation
from src.depends.usecases import (
    get_create_pdf_ticket_interactor,
    get_create_user_ticket_interactor,
    get_login_interactor,
    get_register_interactor,
    get_send_pdf_ticket_to_email_interactor,
)
from src.usecases.create_user_ticket.usecase import CreateUserTicket
from src.usecases.tickets.email.usecase import SendPdfTicketToEmail
from src.usecases.tickets.pdf.usecase import CreatePdfTicket
from src.usecases.user.login import Login
from src.usecases.user.register import Register
from src.web.routes.base import user_required
from src.web.schemas.user import CreateUserTicketRequest, LoginRequest, RegisterRequest

router = APIRouter(prefix="", tags=["user"])


@router.post("/user-ticket/", status_code=201)
@user_required
async def add_user_ticket(
    user: UserAnnotation,
    data: CreateUserTicketRequest,
    usecase: Annotated[CreateUserTicket, Depends(get_create_user_ticket_interactor)],
):
    return await usecase(data.ticket_id, data.passangers, user)


@router.get("/pdf-ticket", status_code=200)
@user_required
async def generate_pdf_ticket(
    user: UserAnnotation,
    user_ticket_id: int,
    usecase: Annotated[CreatePdfTicket, Depends(get_create_pdf_ticket_interactor)],
):
    file_content = await usecase(user_ticket_id, user)

    headers = {"Content-Disposition": "attachment; filename=my_bytes_file.pdf"}
    return Response(content=file_content, media_type="text/plain", headers=headers)


@router.get("/pdf-ticket-email", status_code=200)
@user_required
async def send_pdf_ticket_on_email(
    user: UserAnnotation,
    user_ticket_id: int,
    usecase: Annotated[SendPdfTicketToEmail, Depends(get_send_pdf_ticket_to_email_interactor)],
):
    return await usecase(user_ticket_id, user)


@router.post("/register", status_code=201)
async def register(
    request: Request, data: RegisterRequest, usecase: Annotated[Register, Depends(get_register_interactor)]
):
    access_token = await usecase(data)
    request.session.update({"token": access_token})
    return access_token


@router.post("/login", status_code=200)
async def login(request: Request, data: LoginRequest, usecase: Annotated[Login, Depends(get_login_interactor)]):
    access_token = await usecase(data.email, data.password)
    request.session.update({"token": access_token})
    return access_token
