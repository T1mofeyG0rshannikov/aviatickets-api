import httpx


class BaseHttpClient:
    def __init__(self, session: httpx.AsyncClient) -> None:
        self.session = session
