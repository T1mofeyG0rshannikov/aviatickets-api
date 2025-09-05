from src.infrastructure.admin.model_views.base import BaseModelView
from src.infrastructure.persistence.db.models.models import PassengerOrm, UserTicketOrm


class UserTicketAdmin(BaseModelView, model=UserTicketOrm):  # type: ignore
    column_list = [
        UserTicketOrm.id,
        UserTicketOrm.user,
        UserTicketOrm.ticket,
    ]

    page_size = 100

    name = "Билет пользователя"
    name_plural = "Билеты пользователей"

    column_default_sort = ("id", "desc")


class PassengerAdmin(BaseModelView, model=PassengerOrm):  # type: ignore
    column_list = [PassengerOrm.id]
