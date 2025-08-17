from typing import Annotated

from fastapi import Depends

from src.depends.depends import get_jwt_processor
from src.infrastructure.jwt.jwt_processor import JwtProcessor

JwtProcessorAnnotation = Annotated[JwtProcessor, Depends(get_jwt_processor)]
