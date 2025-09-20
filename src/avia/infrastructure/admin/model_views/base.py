from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin import ModelView, action
from sqladmin.helpers import slugify_class_name
from sqlalchemy import delete


class BaseModelView(ModelView):
    page_size = 100

    @action(name="delete_all", label="Удалить", confirmation_message="Вы уверены?")
    async def delete_all_action(self, request: Request):
        async with self.session_maker(expire_on_commit=False) as session:
            await session.execute(delete(self.model))
            await session.commit()
            return RedirectResponse(url=f"/admin/{slugify_class_name(self.model.__name__)}/list", status_code=303)
