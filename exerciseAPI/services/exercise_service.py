from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from exerciseAPI.models import Exercise
from exerciseAPI.schemas.exercise import ExerciseCreate, ExerciseUpdate

from .base_service import BaseService


class ExerciseService(BaseService[Exercise, ExerciseCreate, ExerciseUpdate]):
    async def get_multi_by_lesson(
        self, db: AsyncSession, *, lesson_id: int, skip: int = 0, limit: int = 100
    ) -> List[Exercise]:
        """
        Obtiene una lista de ejercicios para una lección específica.
        """
        result = await db.execute(
            select(self.model)
            .filter(Exercise.lesson_id == lesson_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


exercise_service = ExerciseService(Exercise)
