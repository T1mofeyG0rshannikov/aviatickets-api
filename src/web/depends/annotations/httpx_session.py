from typing import Annotated

import httpx
from fastapi import Depends

from src.infrastructure.depends.base import get_httpx_session

HttpxSessionAnnotation = Annotated[httpx.AsyncClient, Depends(get_httpx_session)]
