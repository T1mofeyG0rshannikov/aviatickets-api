from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import db_generator

DbAnnotation = Annotated[AsyncSession, Depends(db_generator)]
