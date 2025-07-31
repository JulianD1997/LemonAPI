from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Load

from exerciseAPI.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)  # type: ignore
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
        self, db: AsyncSession, id: Any, options: Optional[List[Load]] = None
    ) -> Optional[ModelType]:
        query = select(self.model).filter(self.model.id == id)
        if options:
            query = query.options(*options)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100, **kwargs: Any
    ) -> list[ModelType]:
        """
        Obtiene múltiples registros con filtros dinámicos.
        """
        statement = select(self.model)

        for key, value in kwargs.items():

            if value is not None:

                if hasattr(self.model, key):
                    statement = statement.where(getattr(self.model, key) == value)
                else:
                    warning_message = (
                        f"Advertencia: El modelo {self.model.__name__} "
                        f"no tiene el atributo '{key}' para filtrar."
                    )
                    print(warning_message)

        statement = statement.offset(skip).limit(limit)
        result = await db.execute(statement)
        return result.scalars().all()

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        update_data = obj_in
        if isinstance(obj_in, BaseModel):
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        result = await db.execute(select(self.model).filter(self.model.id == id))
        obj = result.scalars().first()
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj
