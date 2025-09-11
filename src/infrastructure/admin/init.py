from fastapi import FastAPI

from src.infrastructure.admin.admin import CustomAdmin
from src.infrastructure.admin.model_views.airline import AirlineAdmin
from src.infrastructure.admin.model_views.airport import AirportAdmin
from src.infrastructure.admin.model_views.city import CityAdmin
from src.infrastructure.admin.model_views.country import CountryAdmin
from src.infrastructure.admin.model_views.insurance import (
    InsuranceAdmin,
    InsurancePdfAdmin,
)
from src.infrastructure.admin.model_views.region import RegionAdmin
from src.infrastructure.admin.model_views.ticket import (
    TicketAdmin,
    TicketItineraryAdmin,
    TicketSegmentAdmin,
)
from src.infrastructure.admin.model_views.user import UserAdmin
from src.infrastructure.admin.model_views.user_ticket import (
    PassengerAdmin,
    UserTicketAdmin,
    UserTicketPdfAdmin,
)
from src.infrastructure.depends.base import InfraDIContainer
from src.infrastructure.persistence.db.database import engine


def init_admin(app: FastAPI) -> None:
    authentication_backend = InfraDIContainer.admin_auth()
    admin = CustomAdmin(
        app=app,
        engine=engine,
        authentication_backend=authentication_backend,
        templates_dir="src/infrastructure/admin/templates",
    )

    admin.add_view(AirportAdmin)
    admin.add_view(AirlineAdmin)
    admin.add_view(TicketAdmin)
    admin.add_view(TicketItineraryAdmin)
    admin.add_view(TicketSegmentAdmin)
    admin.add_view(UserTicketAdmin)
    admin.add_view(UserAdmin)
    admin.add_view(RegionAdmin)
    admin.add_view(CityAdmin)
    admin.add_view(CountryAdmin)
    admin.add_view(PassengerAdmin)
    admin.add_view(UserTicketPdfAdmin)
    admin.add_view(InsuranceAdmin)
    admin.add_view(InsurancePdfAdmin)
