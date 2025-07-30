from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from exerciseAPI.api.v1.dependencies import get_object_or_404
from exerciseAPI.api.v1.utils import create_response
from exerciseAPI.core.database import get_db
from exerciseAPI.models import Exercise, Lesson, Topic
from exerciseAPI.schemas.exercise import (
    ExerciseCreate,
    ExerciseDetailOut,
    ExerciseOut,
    ExerciseUpdate,
)
from exerciseAPI.schemas.response import ResponseBase
from exerciseAPI.services.exercise_service import exercise_service
from exerciseAPI.services.lesson_service import lesson_service

router = APIRouter()


get_exercise_details_or_404 = get_object_or_404(
    exercise_service,
    param_name="exercise_id",
    options=[
        joinedload(Exercise.lesson).joinedload(Lesson.topic).joinedload(Topic.course),
        selectinload(Exercise.options),
    ],
)

get_exercise_with_options_or_404 = get_object_or_404(
    exercise_service,
    param_name="exercise_id",
    options=[selectinload(Exercise.options)],
)


@router.post(
    "/",
    response_model=ResponseBase[ExerciseOut],
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo ejercicio",
)
async def create_exercise(
    exercise_create: ExerciseCreate, db: AsyncSession = Depends(get_db)
):
    """
    Crea un nuevo ejercicio asociado a una lección.

    - **Valida** que la lección (`lesson_id`) exista.
    - **Crea** el ejercicio de forma asíncrona.
    - **Retorna** el ejercicio recién creado con sus opciones.
    """
    lesson = await lesson_service.get(db=db, id=exercise_create.lesson_id)
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La lección con id {exercise_create.lesson_id} no existe.",
        )
    new_exercise = await exercise_service.create(db=db, obj_in=exercise_create)
    exercise_out = ExerciseOut.model_validate(new_exercise, from_attributes=True)

    return create_response(
        data=[exercise_out],
        message="Ejercicio creado con éxito",
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/",
    response_model=ResponseBase[ExerciseOut],
    summary="Obtener ejercicios (con filtro opcional por lección)",
)
async def get_exercises(
    db: AsyncSession = Depends(get_db),
    lesson_id: Optional[int] = Query(
        default=None, description="Filtrar ejercicios por ID de lección"
    ),
    topic_id: Optional[int] = Query(
        default=None, description="Filtrar ejercicios por ID de tema"
    ),
    course_id: Optional[int] = Query(
        default=None, description="Filtrar ejercicios por ID de curso"
    ),
    page: int = Query(default=1, ge=1, description="Número de página"),
    limit: int = Query(default=10, ge=1, le=100, description="Ejercicios por página"),
):
    """
    Obtiene una lista paginada de ejercicios.

    - Si se provee `lesson_id`, filtra los ejercicios para esa lección.
    - De lo contrario, devuelve todos los ejercicios.
    - Soporta paginación a través de `page` y `limit`.
    """
    skip = (page - 1) * limit
    if lesson_id is not None:
        exercises_orm = await exercise_service.get_multi_by_lesson(
            db, lesson_id=lesson_id, skip=skip, limit=limit
        )
    elif topic_id is not None:
        exercises_orm = await exercise_service.get_multi_by_topic(
            db, topic_id=topic_id, skip=skip, limit=limit
        )
    elif course_id is not None:
        exercises_orm = await exercise_service.get_multi_by_course(
            db, course_id=course_id, skip=skip, limit=limit
        )
    else:
        exercises_orm = await exercise_service.get_multi(db, skip=skip, limit=limit)

    exercises_out = [
        ExerciseOut.model_validate(ex, from_attributes=True) for ex in exercises_orm
    ]
    if len(exercises_out) == 0:
        return create_response(
            data=[],
            message="No se encontraron ejercicios.",
        )
    return create_response(data=exercises_out, message="Ejercicios obtenidos con éxito")


@router.get(
    "/{exercise_id}",
    response_model=ResponseBase[ExerciseDetailOut],
    summary="Obtener un ejercicio por ID",
)
async def get_exercise(exercise: Exercise = Depends(get_exercise_details_or_404)):
    """
    Obtiene un único ejercicio por su ID usando la dependencia,
    incluyendo sus opciones y relaciones anidadas.
    """
    print(f"Obteniendo ejercicio con ID: {exercise.id}")
    print(f"Ejercicio: {exercise}")
    exercise_out = ExerciseDetailOut.model_validate(exercise, from_attributes=True)
    return create_response(data=[exercise_out], message="Ejercicio obtenido con éxito")


@router.put(
    "/{exercise_id}",
    response_model=ResponseBase[ExerciseOut],
    summary="Actualizar un ejercicio por ID",
)
async def update_exercise(
    exercise_update: ExerciseUpdate,
    exercise_to_update: Exercise = Depends(
        get_object_or_404(exercise_service, "exercise_id")
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Actualiza la información de un ejercicio existente de forma asíncrona.
    """
    updated_exercise = await exercise_service.update(
        db=db, db_obj=exercise_to_update, obj_in=exercise_update
    )
    exercise_out = ExerciseOut.model_validate(updated_exercise, from_attributes=True)
    return create_response(
        data=[exercise_out], message="Ejercicio actualizado con éxito"
    )


@router.delete(
    "/{exercise_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un ejercicio por ID",
)
async def delete_exercise(
    exercise_to_delete: Exercise = Depends(get_exercise_with_options_or_404),
    db: AsyncSession = Depends(get_db),
):
    """
    Elimina un ejercicio de la base de datos de forma asíncrona.
    """
    await exercise_service.remove(db=db, id=exercise_to_delete.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
