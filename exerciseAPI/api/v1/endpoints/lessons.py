from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from models import Lesson, Topic
from schemas.lesson import LessonCreate, LessonOut, LessonUpdate
from schemas.response import ResponseBase, common_response
from settings.database.config import get_db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

router = APIRouter()


@router.post(
    "/",
    response_model=ResponseBase,
    status_code=status.HTTP_201_CREATED,
    responses={201: common_response[201], 500: common_response[500]},
)
async def create_lesson(
    lesson_create: LessonCreate,
    db: Session = Depends(get_db),
):
    """
    Crear una nueva lección para un tema.
    """
    try:
        topic = db.query(Topic).filter(Topic.id == lesson_create.topic_id).first()
        if not topic:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Tema no encontrado",
                success=False,
            )

        new_lesson = Lesson(**lesson_create.model_dump())
        db.add(new_lesson)
        db.commit()
        db.refresh(new_lesson)
        return ResponseBase(
            status_code=status.HTTP_201_CREATED,
            message="Lección creada con éxito",
            success=True,
        )
    except SQLAlchemyError:
        db.rollback()
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al crear la lección",
            success=False,
        )


@router.get(
    "/",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={200: common_response[200], 500: common_response[500]},
)
async def get_lessons(
    topic_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()

        if not topic:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Tema no encontrado",
                success=False,
            )

        query = db.query(Lesson.id, Lesson.name, Topic.name.label("topic_name")).join(
            Lesson.topic
        )
        if topic_id:
            query = query.filter(Topic.id == topic_id)
        result = query.all()

        lessons = [
            LessonOut(
                id=row.id,
                name=row.name,
                topic_name=row.topic_name,
            )
            for row in result
        ]

        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Lecciones obtenidas con éxito",
            success=True,
            results=lessons,
        )
    except SQLAlchemyError:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al obtener las lecciones",
            success=False,
        )


@router.get(
    "/{lesson_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={
        200: common_response[200],
        404: common_response[404],
        500: common_response[500],
    },
)
async def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una lección por ID.
    """
    try:
        result = (
            db.query(Lesson.id, Lesson.name, Topic.name.label("topic_name"))
            .join(Lesson.topic)
            .filter(Lesson.id == lesson_id)
            .first()
        )
        if not result:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="lección no encontrado",
                success=False,
            )
        lesson = LessonOut.model_validate(result, from_attributes=True)
        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Lección obtenida con éxito",
            success=True,
            results=[lesson],
        )
    except SQLAlchemyError:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al obtener la lección",
            success=False,
        )


@router.put(
    "/{lesson_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={
        200: common_response[200],
        404: common_response[404],
        500: common_response[500],
    },
)
async def update_lesson(
    lesson_id: int, lesson_update: LessonUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza una lección por ID.
    """
    try:
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if not lesson:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Lección no encontrada",
                success=False,
            )
        lesson.name = lesson_update.name
        lesson.topic_id = lesson_update.topic_id
        db.commit()
        db.refresh(lesson)
        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Lección actualizada con éxito",
            success=True,
        )
    except SQLAlchemyError:
        db.rollback()
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al actualizar la lección",
            success=False,
        )


@router.delete(
    "/{lesson_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={
        200: common_response[200],
        404: common_response[404],
        500: common_response[500],
    },
)
async def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """
    Elimina una lección por ID.
    """
    try:
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        if not lesson:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Lección no encontrada",
                success=False,
            )
        db.delete(lesson)
        db.commit()
        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Lección eliminada con éxito",
            success=True,
        )
    except SQLAlchemyError:
        db.rollback()
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al eliminar la lección",
            success=False,
        )
