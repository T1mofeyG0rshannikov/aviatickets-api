from io import BytesIO
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse, StreamingResponse

from avia.application.dto.user import RegisterUserDTO, UserDTO
from avia.application.dto.user_ticket import CreatePassengerDTO
from avia.application.usecases.create_user_ticket import CreateUserTicket
from avia.application.usecases.insurance.create import CreateInsurance
from avia.application.usecases.insurance.get_pdf import GetPdfInsurance
from avia.application.usecases.tickets.email import SendPdfTicketToEmail
from avia.application.usecases.tickets.pdf.get import GetPdfTicket
from avia.application.usecases.user.auth.login import Login
from avia.application.usecases.user.auth.register import Register
from avia.entities.exceptions import AccessDeniedError
from avia.entities.user.exceptions import (
    InvalidEmailError,
    InvalidFirstNameError,
    InvalidPasswordError,
    UserNotFoundError,
    UserWithEmailAlreadyExistError,
)
from avia.entities.user.value_objects.email import Email
from avia.entities.user.value_objects.password import Password
from avia.entities.user_ticket.exceptions import (
    ExpiredInternationalPassportError,
    InvalidInternationalPassportError,
)
from avia.entities.value_objects.entity_id import EntityId
from avia.web.depends.annotations.user_annotation import UserAnnotation
from avia.web.depends.usecases import (
    get_create_insurance_interactor,
    get_create_user_ticket_interactor,
    get_login_interactor,
    get_pdf_insurance_interactor,
    get_pdf_ticket_interactor,
    get_register_interactor,
    get_send_pdf_ticket_to_email_interactor,
)
from avia.web.routes.base import user_required
from avia.web.schemas.login import LoginResponse
from avia.web.schemas.user import CreateUserTicketRequest, LoginRequest, RegisterRequest

router = APIRouter(prefix="", tags=["user"])


@router.post("/user-ticket/", status_code=201)
@user_required
async def add_user_ticket(
    user: UserAnnotation,
    data: CreateUserTicketRequest,
    usecase: Annotated[CreateUserTicket, Depends(get_create_user_ticket_interactor)],
):
    try:
        passengers_dto = [CreatePassengerDTO(**passenger.model_dump()) for passenger in data.passengers]

        user_ticket_id = await usecase(EntityId(data.ticket_id), passengers_dto, user)
        return JSONResponse(status_code=201, content={"user_ticket_id": str(user_ticket_id.value)})

    except InvalidInternationalPassportError as e:
        error_string = str(e)

        passenger = error_string.split(":")[0]
        error_message = error_string.split(":")[1].split("-")[0].strip()

        return JSONResponse(status_code=400, content={"errors": {passenger: {"passport": error_message}}})

    except ExpiredInternationalPassportError as e:
        error_string = str(e)

        passenger = error_string.split(":")[0]
        error_message = error_string.split(":")[1].split("-")[0].strip()

        return JSONResponse(status_code=400, content={"errors": {passenger: {"expiration_date": error_message}}})


@router.get("/pdf-ticket", status_code=200, response_class=StreamingResponse)
@user_required
async def get_pdf_ticket(
    user: UserAnnotation,
    user_ticket_id: UUID,
    usecase: Annotated[GetPdfTicket, Depends(get_pdf_ticket_interactor)],
):
    file = await usecase(EntityId(user_ticket_id), user)
    headers = {"Content-Disposition": f"attachment; filename={file.name}"}
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
    try:
        access_token = await usecase(RegisterUserDTO(**data.__dict__))
        request.session.update({"token": access_token})
        return access_token
    except (InvalidEmailError, UserWithEmailAlreadyExistError) as e:
        return JSONResponse(status_code=400, content={"errors": {"email": str(e)}})
    except InvalidFirstNameError as e:
        return JSONResponse(status_code=400, content={"errors": {"firstName": str(e)}})


@router.post("/login", status_code=200, response_model=LoginResponse)
async def login(
    request: Request, data: LoginRequest, usecase: Annotated[Login, Depends(get_login_interactor)]
) -> LoginResponse:
    try:
        access_token = await usecase(Email(data.email), Password(data.password))
        request.session.update({"token": access_token})
        return LoginResponse(access_token=access_token)
    except InvalidPasswordError as e:
        return JSONResponse(status_code=403, content={"errors": {"password": str(e)}})
    except UserNotFoundError as e:
        return JSONResponse(status_code=404, content={"errors": {"email": str(e)}})


@router.get("/pdf-insurance", status_code=200, response_class=StreamingResponse)
@user_required
async def get_pdf_insurance(
    user: UserAnnotation,
    insurance_id: UUID,
    usecase: Annotated[GetPdfInsurance, Depends(get_pdf_insurance_interactor)],
) -> StreamingResponse:
    try:
        file = await usecase(EntityId(insurance_id), user)
        headers = {"Content-Disposition": f"attachment; filename={file.name}"}
        return StreamingResponse(BytesIO(file.content), media_type="application/pdf", headers=headers)
    except AccessDeniedError as e:
        return JSONResponse(status_code=403, content={"message": str(e)})


@router.post("/insurance", status_code=201)
@user_required
async def create_insurance(
    user: UserAnnotation,
    user_ticket_id: UUID,
    usecase: Annotated[CreateInsurance, Depends(get_create_insurance_interactor)],
):
    insurance = await usecase(EntityId(user_ticket_id), user)
    return JSONResponse(status_code=201, content={"insurance_id": str(insurance.id.value)})


@router.get("/user", status_code=200)
async def get_user(user: UserAnnotation):
    return UserDTO.from_entity(user) if user else None
