from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.entities.exceptions import (
    AccessDeniedError,
    InvalidCreditnailsError,
    RecordNotFoundException,
)


async def record_not_found_exc_handler(request: Request, exc: RecordNotFoundException) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": str(exc)})


async def access_denied_exc_handler(request: Request, exc: AccessDeniedError) -> JSONResponse:
    return JSONResponse(status_code=403, content={"message": str(exc)})


async def invalid_creditnails_exc_handler(request: Request, exc: InvalidCreditnailsError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"message": str(exc)})


def init_exc_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RecordNotFoundException, record_not_found_exc_handler)
    app.add_exception_handler(AccessDeniedError, access_denied_exc_handler)
    app.add_exception_handler(InvalidCreditnailsError, invalid_creditnails_exc_handler)
