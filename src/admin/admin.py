from fastapi import Request, Response
from sqladmin import Admin
from starlette.responses import RedirectResponse


class CustomAdmin(Admin):
    async def login(self, request: Request) -> Response:
        assert self.authentication_backend is not None

        context = {}
        if request.method == "GET":
            return await self.templates.TemplateResponse(request, "sqladmin/login.html")

        response = await self.authentication_backend.login(request)
        if not response.ok:
            context["email_error_message"] = response.email_error_message
            context["password_error_message"] = response.password_error_message
            return await self.templates.TemplateResponse(request, "sqladmin/login.html", context, status_code=400)

        return RedirectResponse(request.url_for("admin:index"), status_code=302)
