from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from src.infrastructure.admin.init import init_admin
from src.infrastructure.depends.base import InfraDIContainer
from src.web.exc_handler import init_exc_handlers
from src.web.routes.tickets_route import router as tickets_router
from src.web.routes.user_route import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_admin(app)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    SessionMiddleware, secret_key=InfraDIContainer.admin_config().secret_key, same_site="lax", https_only=True
)

origins = ["http://localhost:3001"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=user_router)
app.include_router(router=tickets_router)
init_exc_handlers(app)
