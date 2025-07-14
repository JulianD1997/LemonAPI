from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from exerciseAPI.models import Lesson
from exerciseAPI.schemas.lesson import LessonCreate, LessonUpdate

from .base_service import BaseService


class LessonService(BaseService[Lesson, LessonCreate, LessonUpdate]):
    async def get_multi_by_topic(
        self, db: AsyncSession, *, topic_id: int, skip: int = 0, limit: int = 100
    ) -> List[Lesson]:
        """
        Obtiene una lista de lecciones para un tema específico.
        """
        result = await db.execute(
            select(self.model)
            .filter(Lesson.topic_id == topic_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


lesson_service = LessonService(Lesson)
