from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from avia.infrastructure.persistence.db.database import db_generator

DbAnnotation = Annotated[AsyncSession, Depends(db_generator)]
