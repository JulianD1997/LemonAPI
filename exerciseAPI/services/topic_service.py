from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from exerciseAPI.models import Topic
from exerciseAPI.schemas.topic import TopicCreate, TopicUpdate

from .base_service import BaseService


class TopicService(BaseService[Topic, TopicCreate, TopicUpdate]):
    async def get_multi_by_course(
        self, db: AsyncSession, *, course_id: int, skip: int = 0, limit: int = 100
    ) -> List[Topic]:
        """
        Obtiene una lista de temas para un curso específico.
        """
        result = await db.execute(
            select(self.model)
            .filter(Topic.course_id == course_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


topic_service = TopicService(Topic)
