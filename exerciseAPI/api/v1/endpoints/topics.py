from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from models import Course, Topic
from schemas.response import ResponseBase, common_response
from schemas.topic import TopicCreate, TopicOut, TopicUpdate
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
async def create_topic(topic_create: TopicCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo tema para un curso.
    """
    try:
        course = db.query(Course).filter(Course.id == topic_create.course_id).first()
        if not course:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Curso no encontrado",
                success=False,
            )

        new_topic = Topic(**topic_create.model_dump())
        db.add(new_topic)
        db.commit()
        db.refresh(new_topic)
        return ResponseBase(
            status_code=status.HTTP_201_CREATED,
            message="Tema creado con éxito",
            success=True,
        )
    except SQLAlchemyError:
        db.rollback()
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al crear el tema",
            success=False,
        )


@router.get(
    "/",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={200: common_response[200], 500: common_response[500]},
)
async def get_topics(
    course_name: Optional[str] = Query(default=None),
    course_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
):
    """
    Obtiene todos los temas con el nombre de su curso.
    """
    try:
        course = (
            db.query(Course).filter(Course.id == course_id).first()
            if course_id
            else db.query(Course).filter(Course.name == course_name).first()
        )
        if not course:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Curso no encontrado",
                success=False,
            )

        query = db.query(Topic.id, Topic.name, Course.name.label("course_name")).join(
            Topic.course
        )

        if course_name:
            query = query.filter(Course.name.ilike(f"{course_name}%"))
        if course_id:
            query = query.filter(Course.id == course_id)

        result = query.all()

        topics = [
            TopicOut(
                id=row.id,
                name=row.name,
                course_name=row.course_name,
            )
            for row in result
        ]

        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Temas obtenidos con éxito",
            success=True,
            results=topics,
        )
    except SQLAlchemyError:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al obtener los temas",
            success=False,
        )


@router.get(
    "/{topic_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={
        200: common_response[200],
        404: common_response[404],
        500: common_response[500],
    },
)
async def get_topic(topic_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un tema por ID (optimizado).
    """
    try:
        result = (
            db.query(
                Topic.id, Topic.name, Course.name.label("course_name")
            )
            .join(Topic.course)
            .filter(Topic.id == topic_id)
            .first()
        )
        if not result:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Tema no encontrado",
                success=False,
            )
        topic = TopicOut.model_validate(result, from_attributes=True)
        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Tema obtenido con éxito",
            success=True,
            results=[topic],
        )
    except SQLAlchemyError:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al obtener el tema",
            success=False,
        )


@router.put(
    "/{topic_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={
        200: common_response[200],
        404: common_response[404],
        500: common_response[500],
    },
)
async def update_topic(
    topic_id: int, topic_update: TopicUpdate, db: Session = Depends(get_db)
):
    """
    Actualiza un tema por ID.
    """
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Tema no encontrado",
                success=False,
            )
        topic.name = topic_update.name
        topic.course_id = topic_update.course_id
        db.commit()
        db.refresh(topic)
        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Tema actualizado con éxito",
            success=True,
        )
    except SQLAlchemyError:
        db.rollback()
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al actualizar el tema",
            success=False,
        )


@router.delete(
    "/{topic_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    responses={
        200: common_response[200],
        404: common_response[404],
        500: common_response[500],
    },
)
async def delete_topic(topic_id: int, db: Session = Depends(get_db)):
    """
    Elimina un tema por ID.
    """
    try:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return ResponseBase(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Tema no encontrado",
                success=False,
            )
        db.delete(topic)
        db.commit()
        return ResponseBase(
            status_code=status.HTTP_200_OK,
            message="Tema eliminado con éxito",
            success=True,
        )
    except SQLAlchemyError:
        db.rollback()
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Error al eliminar el tema",
            success=False,
        )
