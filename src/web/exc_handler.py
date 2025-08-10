from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.entities.exceptions import NotPermittedError, RecordNotFoundException


async def record_not_found_exc_handler(request: Request, exc: RecordNotFoundException) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": str(exc)})


async def not_permitted_exc_handler(request: Request, exc: NotPermittedError) -> JSONResponse:
    return JSONResponse(status_code=403, content={"message": str(exc)})


def init_exc_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RecordNotFoundException, record_not_found_exc_handler)
    app.add_exception_handler(NotPermittedError, not_permitted_exc_handler)
