from typing import List

from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin import ModelView, action
from sqladmin.helpers import slugify_class_name
from sqladmin.pagination import Pagination
from sqlalchemy import and_, delete, func, select
from sqlalchemy.orm import selectinload


class BaseModelView(ModelView):
    diapazon_filter_fields = []
    page_size = 100

    @action(name="delete_all", label="Удалить", confirmation_message="Вы уверены?")
    async def delete_all_action(self, request: Request):
        async with self.session_maker(expire_on_commit=False) as session:
            await session.execute(delete(self.model))
            await session.commit()
            return RedirectResponse(url=f"/admin/{slugify_class_name(self.model.__name__)}/list", status_code=303)


def format_sum(num: float) -> str:
    if abs(num) // 1_000_000 > 0:
        num = round(num / 1_000_000, 1)
        if num == int(num):
            num = int(num)
        return f"{num}M"
    if abs(num) // 1_000 > 0:
        num = round(num / 1_000, 1)
        if num == int(num):
            num = int(num)
        return f"{num}K"

    num = round(num, 2)
    if num == int(num):
        num = int(num)
    return str(num)


DEGREES_COLORS = {"more": "(20, 215, 20)", "less": "(255, 100, 100)"}


def render_profit(value: int | None) -> str:
    if value is None:
        return ""

    if value == 0:
        return ""

    value_format = format_sum(value)

    return f"""<span style="color: rgb{DEGREES_COLORS["more" if value > 0 else "less"]}">{value_format}</span>"""


def render_degrees(value: int | None) -> str:
    if value is None:
        return ""

    if value == 0:
        return ""

    value_format = format_sum(value)

    return f"""<span style="color: rgb{DEGREES_COLORS["more" if value > 0 else "less"]}">({value_format if value < 0 else f"+{value_format}"})</span>"""
