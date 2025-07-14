from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from exerciseAPI.api.v1.dependencies import get_object_or_404
from exerciseAPI.api.v1.utils import create_response
from exerciseAPI.core.database import get_db
from exerciseAPI.models import Lesson
from exerciseAPI.schemas.lesson import LessonCreate, LessonOut, LessonUpdate
from exerciseAPI.schemas.response import ResponseBase
from exerciseAPI.services.lesson_service import lesson_service
from exerciseAPI.services.topic_service import topic_service

router = APIRouter()

get_lesson_or_404 = get_object_or_404(lesson_service)


@router.post(
    "/",
    response_model=ResponseBase[LessonOut],
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva lección",
)
async def create_lesson(
    lesson_create: LessonCreate, db: AsyncSession = Depends(get_db)
):
    """
    Crea una nueva lección asociada a un tema.

    - **Valida** que el tema (`topic_id`) exista.
    - **Crea** la lección de forma asíncrona.
    - **Retorna** la lección recién creada.
    """
    topic = await topic_service.get(db=db, id=lesson_create.topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El tema con id {lesson_create.topic_id} no existe.",
        )

    new_lesson = await lesson_service.create(db=db, obj_in=lesson_create)
    lesson_out = LessonOut.model_validate(new_lesson, from_attributes=True)

    return create_response(
        data=[lesson_out],
        message="Lección creada con éxito",
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/",
    response_model=ResponseBase[LessonOut],
    summary="Obtener lecciones (con filtro opcional por tema)",
)
async def get_lessons(
    db: AsyncSession = Depends(get_db),
    topic_id: Optional[int] = Query(
        default=None, description="Filtrar lecciones por ID de tema"
    ),
):
    """
    Obtiene una lista de lecciones.

    - Si se provee `topic_id`, filtra las lecciones para ese tema.
    - De lo contrario, devuelve todas las lecciones (considerar paginación aquí).
    """
    if topic_id is not None:
        lessons_orm = await lesson_service.get_multi_by_topic(db, topic_id=topic_id)
    else:
        lessons_orm = await lesson_service.get_multi(db, limit=100)

    lessons_out = [
        LessonOut.model_validate(ln, from_attributes=True) for ln in lessons_orm
    ]
    return create_response(data=lessons_out, message="Lecciones obtenidas con éxito")


@router.get(
    "/{lesson_id}",
    response_model=ResponseBase[LessonOut],
    summary="Obtener una lección por ID",
)
async def get_lesson(lesson: Lesson = Depends(get_lesson_or_404)):
    """
    Obtiene una única lección por su ID usando la dependencia.
    """
    lesson_out = LessonOut.model_validate(lesson, from_attributes=True)
    return create_response(data=[lesson_out], message="Lección obtenida con éxito")


@router.put(
    "/{lesson_id}",
    response_model=ResponseBase[LessonOut],
    summary="Actualizar una lección por ID",
)
async def update_lesson(
    lesson_update: LessonUpdate,
    lesson_to_update: Lesson = Depends(get_lesson_or_404),
    db: AsyncSession = Depends(get_db),
):
    """
    Actualiza la información de una lección existente de forma asíncrona.
    """
    updated_lesson = await lesson_service.update(
        db=db, db_obj=lesson_to_update, obj_in=lesson_update
    )
    lesson_out = LessonOut.model_validate(updated_lesson, from_attributes=True)
    return create_response(data=[lesson_out], message="Lección actualizada con éxito")


@router.delete(
    "/{lesson_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una lección por ID",
)
async def delete_lesson(
    lesson_to_delete: Lesson = Depends(get_lesson_or_404),
    db: AsyncSession = Depends(get_db),
):
    """
    Elimina una lección de la base de datos de forma asíncrona.
    """
    await lesson_service.remove(db=db, id=lesson_to_delete.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
