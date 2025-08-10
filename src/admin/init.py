from fastapi import FastAPI

from src.admin.admin import CustomAdmin
from src.admin.auth import AdminAuth
from src.admin.model_views.airline import AirlineAdmin
from src.admin.model_views.airport import AirportAdmin
from src.admin.model_views.city import CityAdmin
from src.admin.model_views.country import CountryAdmin
from src.admin.model_views.region import RegionAdmin
from src.admin.model_views.ticket import TicketAdmin
from src.admin.model_views.views import UserAdmin
from src.db.database import engine
from src.depends.depends import get_admin_config, get_jwt_processor, get_password_hasher


def init_admin(app: FastAPI) -> None:
    authentication_backend = AdminAuth(
        jwt_processor=get_jwt_processor(), password_hasher=get_password_hasher(), config=get_admin_config()
    )
    admin = CustomAdmin(
        app=app, engine=engine, authentication_backend=authentication_backend, templates_dir="src/admin/templates"
    )

    admin.add_view(AirportAdmin)
    admin.add_view(AirlineAdmin)
    admin.add_view(TicketAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(RegionAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(CountryAdmin)
