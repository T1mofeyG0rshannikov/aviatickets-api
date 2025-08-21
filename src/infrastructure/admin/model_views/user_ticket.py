from src.infrastructure.admin.model_views.base import BaseModelView
from src.infrastructure.db.models.models import PassengerOrm, UserTicketOrm


class UserTicketAdmin(BaseModelView, model=UserTicketOrm):
    column_list = [
        UserTicketOrm.id,
        UserTicketOrm.user,
        UserTicketOrm.ticket,
    ]

    page_size = 100

    name = "Билет пользователя"
    name_plural = "Билеты пользователей"

    column_default_sort = ("id", "desc")


class PassangerAdmin(BaseModelView, model=PassengerOrm):
    column_list = [PassengerOrm.id]
