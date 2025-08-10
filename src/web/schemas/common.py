from pydantic import BaseModel


class DeviceRequest(BaseModel):
    app_id: str
    auth_token: str


class APIResponse(BaseModel):
    status: str
