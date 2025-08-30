from io import BytesIO
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse

from src.application.dto.user_ticket import CreatePassengerDTO
from src.application.usecases.create_user_ticket import CreateUserTicket
from src.application.usecases.tickets.email import SendPdfTicketToEmail
from src.application.usecases.tickets.pdf.usecase import CreatePdfTicket
from src.application.usecases.user.auth.login import Login
from src.application.usecases.user.auth.register import Register
from src.entities.value_objects.entity_id import EntityId
from src.web.depends.annotations.user_annotation import UserAnnotation
from src.web.depends.usecases import (
    get_create_pdf_ticket_interactor,
    get_create_user_ticket_interactor,
    get_login_interactor,
    get_register_interactor,
    get_send_pdf_ticket_to_email_interactor,
)
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
    passengers_dto = [CreatePassengerDTO(**passenger.model_dump()) for passenger in data.passengers]

    return await usecase(data.ticket_id, passengers_dto, user)


@router.get("/pdf-ticket", status_code=200, response_class=StreamingResponse)
@user_required
async def generate_pdf_ticket(
    user: UserAnnotation,
    user_ticket_id: UUID,
    usecase: Annotated[CreatePdfTicket, Depends(get_create_pdf_ticket_interactor)],
):
    file = await usecase(EntityId(user_ticket_id), user)
    headers = {"Content-Disposition": f"attachment; filename={file.name}.pdf"}
    return StreamingResponse(BytesIO(file.content), media_type="application/pdf", headers=headers)


@router.get("/pdf-ticket-email", status_code=200)
@user_required
async def send_pdf_ticket_on_email(
    user: UserAnnotation,
    user_ticket_id: UUID,
    usecase: Annotated[SendPdfTicketToEmail, Depends(get_send_pdf_ticket_to_email_interactor)],
):
    return await usecase(EntityId(user_ticket_id), user)


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
