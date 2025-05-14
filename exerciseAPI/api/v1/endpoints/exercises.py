from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from models import Exercise, Option
from models.Exercise import ExerciseType
from schemas.exercise import ExerciseCreate, ExerciseDetailOut, ExerciseListOut
from schemas.option import OptionSafeOut
from schemas.response import ResponseBase, common_response
from settings.database.config import get_db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

router = APIRouter()


@router.get(
    "/types",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Lista de tipos de ejercicio"}},
)
async def get_exercise_types():
    return ResponseBase(
        status_code=status.HTTP_200_OK,
        message="Ejercicio creado con éxito",
        success=True,
        results=[t.value for t in ExerciseType],
    )


@router.post(
    "/",
    response_model=ResponseBase,
    status_code=status.HTTP_201_CREATED,
    responses={201: common_response[201], 500: common_response[500]},
)
async def create_exercise(
    exercise_create: ExerciseCreate, db: Session = Depends(get_db)
):
    try:
        print(exercise_create)
        new_exercise = Exercise(
            title=exercise_create.title,
            ex_type=exercise_create.ex_type,
            exercise_text=exercise_create.exercise_text,
            created_by=exercise_create.created_by,
            lesson_id=exercise_create.lesson_id,
        )

        db.add(new_exercise)
        db.flush()

        for opt in exercise_create.options:
            db.add(
                Option(
                    text=opt.text,
                    is_correct=opt.is_correct,
                    exercise_id=new_exercise.id,
                )
            )

        db.commit()
        db.refresh(new_exercise)

        return ResponseBase(
            status_code=status.HTTP_201_CREATED,
            message="Ejercicio fue creado con éxito",
            success=True,
        )

    except SQLAlchemyError:
        db.rollback()
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al crear el ejercicio",
            success=False,
        )


@router.get(
    "/",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={200: common_response[200], 500: common_response[500]},
)
async def get_exercises(
    page: int = Query(1, ge=1),
    limit: int = Query(6, ge=1),
    lesson_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    try:
        offset = (page - 1) * limit

        query = db.query(Exercise).join(Exercise.lesson)
        if lesson_id:
            query = query.filter(Exercise.lesson_id == lesson_id)

        exercises = query.offset(offset).limit(limit).all()

        results = []
        for e in exercises:
            results.append(
                ExerciseListOut(
                    id=e.id,
                    title=e.title,
                    ex_type=e.ex_type,
                    exercise_text=e.exercise_text,
                    lesson_name=e.lesson.name,
                )
            )

        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Ejercicios obtenidos con éxito",
            success=True,
            results=results,
        )

    except SQLAlchemyError:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al obtener los ejercicios",
            success=False,
        )


@router.get(
    "/{exercise_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={
        200: common_response[200],
        404: common_response[404],
        500: common_response[500],
    },
)
async def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    try:
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Ejercicio no encontrado",
                success=False,
            )

        result = ExerciseDetailOut(
            id=exercise.id,
            title=exercise.title,
            ex_type=exercise.ex_type,
            exercise_text=exercise.exercise_text,
            lesson_name=exercise.lesson.name,
            options=[OptionSafeOut.model_validate(opt) for opt in exercise.options],
        )

        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Ejercicio obtenido con éxito",
            success=True,
            results=[result],
        )

    except SQLAlchemyError:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al obtener el ejercicio",
            success=False,
        )


@router.delete(
    "/{exercise_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={
        200: common_response[200],
        404: common_response[404],
        500: common_response[500],
    },
)
async def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    try:
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        if not exercise:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Ejercicio no encontrado",
                success=False,
            )
        db.delete(exercise)
        db.commit()
        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Ejercicio eliminado con éxito",
            success=True,
        )
    except SQLAlchemyError:
        db.rollback()
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al eliminar el ejercicio",
            success=False,
        )
