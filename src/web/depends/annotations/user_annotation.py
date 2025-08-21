from typing import Annotated

from fastapi import Depends

from src.entities.user.user import User
from src.web.routes.base import get_user

UserAnnotation = Annotated[User, Depends(get_user)]
