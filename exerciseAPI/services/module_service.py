from ast import Module
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from exerciseAPI.models import Exercise
from exerciseAPI.schemas.module import ModuleCreate, ModuleUpdate
from exerciseAPI.services.base_service import BaseService


class ModuleService(BaseService[Module, ModuleCreate, ModuleUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: ModuleCreate) -> Module:
        exercise_ids = obj_in.exercises
        module_data = obj_in.model_dump(exclude={"exercises"})

        db_obj = self.model(**module_data)

        if exercise_ids:
            exercises = await db.execute(
                select(Exercise).where(Exercise.id.in_(exercise_ids))
            )
            db_obj.exercises.extend(exercises.scalars().all())

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_course(
        self, db: AsyncSession, *, course_id: int, skip: int = 0, limit: int = 100
    ) -> List[Module]:
        """
        Obtiene una lista de módulos para un curso específico.
        """
        result = await db.execute(
            select(self.model)
            .filter(self.model.course_id == course_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


module_service = ModuleService(Module)
