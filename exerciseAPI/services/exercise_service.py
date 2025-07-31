from typing import Any, Dict, List, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from exerciseAPI.models import Exercise, Lesson, Option, Topic
from exerciseAPI.schemas.exercise import ExerciseCreate, ExerciseUpdate

from .base_service import BaseService


class ExerciseService(BaseService[Exercise, ExerciseCreate, ExerciseUpdate]):
    async def create(self, db: AsyncSession, *, obj_in: ExerciseCreate) -> Exercise:
        """
        Crea un nuevo ejercicio y sus opciones asociadas.
        Este método sobrescribe el método 'create' de BaseService para manejar
        la creación de las opciones anidadas.
        """

        obj_in_data = obj_in.model_dump()

        obj_in_data.pop("interactive_code", None)
        options_data = obj_in_data.pop("options", [])

        db_obj = self.model(**obj_in_data)

        db_obj.options = [Option(**opt) for opt in options_data]

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        return db_obj

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        lesson_id: Optional[int] = None,
        topic_id: Optional[int] = None,
        course_id: Optional[int] = None,
    ) -> List[Exercise]:
        """
        Obtiene una lista de ejercicios, con la opción de filtrar por lección,
        tema o curso. Los filtros son excluyentes por prioridad.
        """
        query = select(self.model)

        if lesson_id is not None:
            query = query.filter(self.model.lesson_id == lesson_id)
        elif topic_id is not None:
            query = query.join(Lesson).filter(Lesson.topic_id == topic_id)
        elif course_id is not None:
            query = (
                query.join(Lesson, self.model.lesson_id == Lesson.id)
                .join(Topic, Lesson.topic_id == Topic.id)
                .filter(Topic.course_id == course_id)
            )

        query = (
            query.options(selectinload(self.model.options)).offset(skip).limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().unique().all()

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: Exercise,
        obj_in: Union[ExerciseUpdate, Dict[str, Any]],
    ) -> Exercise:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        options_data = update_data.pop("options", None)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        if options_data is not None:
            if "options" not in db_obj.__dict__:
                await db.refresh(db_obj, ["options"])

            existing_options = {option.id: option for option in db_obj.options}
            incoming_option_ids = {
                opt.get("id") for opt in options_data if opt.get("id")
            }

            for option_id, option in existing_options.items():
                if option_id not in incoming_option_ids:
                    await db.delete(option)

            for option_data in options_data:
                option_id = option_data.get("id")
                if option_id and option_id in existing_options:
                    option = existing_options[option_id]
                    for key, value in option_data.items():
                        if value is not None and key != "id":
                            setattr(option, key, value)
                elif not option_id:
                    new_option_data = {
                        k: v
                        for k, v in option_data.items()
                        if k != "id" and v is not None
                    }
                    if "text" in new_option_data and "is_correct" in new_option_data:
                        db_obj.options.append(Option(**new_option_data))

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


exercise_service = ExerciseService(Exercise)
