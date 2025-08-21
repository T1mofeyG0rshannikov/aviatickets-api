from typing import Annotated

from fastapi import Depends

from src.infrastructure.jwt.jwt_processor import JwtProcessor
from src.web.depends.depends import get_jwt_processor

JwtProcessorAnnotation = Annotated[JwtProcessor, Depends(get_jwt_processor)]
