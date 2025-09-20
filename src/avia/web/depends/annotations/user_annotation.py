from typing import Annotated

from fastapi import Depends

from avia.entities.user.user import User
from avia.web.routes.base import get_user

UserAnnotation = Annotated[User, Depends(get_user)]
