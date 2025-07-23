from typing import Callable, List, Optional, TypeVar

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.strategy_options import Load

from exerciseAPI.core.database import Base, get_db
from exerciseAPI.services.base_service import BaseService

ModelType = TypeVar("ModelType", bound=Base)  # type: ignore


def get_object_or_404(
    service: BaseService,
    param_name: str = "course_id",
    options: Optional[List[Load]] = None,
) -> Callable:
    async def _get_object(
        id: int = Path(..., alias=param_name),
        db: AsyncSession = Depends(get_db),
    ) -> ModelType:
        query = select(service.model).filter(service.model.id == id)

        if options:
            for opt in options:
                query = query.options(opt)

        result = await db.execute(query)
        obj = result.scalar_one_or_none()

        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{service.model.__name__} con id {id} no encontrado.",
            )

        return obj

    return _get_object
