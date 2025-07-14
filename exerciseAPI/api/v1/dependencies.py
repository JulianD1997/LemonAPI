from typing import Callable, TypeVar

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from exerciseAPI.core.database import Base, get_db
from exerciseAPI.services.base_service import BaseService

ModelType = TypeVar("ModelType", bound=Base)


def get_object_or_404(service: BaseService) -> Callable:
    """
    Crea una dependencia que obtiene un objeto por su ID o lanza un error 404.
    """

    async def _get_object_by_id(
        item_id: int,
        db: AsyncSession = Depends(get_db),
    ) -> ModelType:
        obj = await service.get(db=db, id=item_id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{service.model.__name__} con id {item_id} no encontrado.",
            )
        return obj

    return _get_object_by_id
