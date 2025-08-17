from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from src.admin.init import init_admin
from src.depends.depends import get_admin_config
from src.web.exc_handler import init_exc_handlers
from src.web.routes.tickets_route import router as tickets_router
from src.web.routes.user_route import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_admin(app)
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="src/web/static"), name="static")

app.add_middleware(SessionMiddleware, secret_key=get_admin_config().admin_secret_key)

app.include_router(router=user_router)
app.include_router(router=tickets_router)
init_exc_handlers(app)
