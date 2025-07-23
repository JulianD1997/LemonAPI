from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from exerciseAPI.api.v1.dependencies import get_object_or_404
from exerciseAPI.api.v1.utils import create_response
from exerciseAPI.core.database import get_db
from exerciseAPI.models import Topic
from exerciseAPI.schemas.response import ResponseBase, common_response
from exerciseAPI.schemas.topic import TopicCreate, TopicOut, TopicUpdate
from exerciseAPI.services.course_service import course_service
from exerciseAPI.services.topic_service import topic_service

router = APIRouter()

get_topic_or_404 = get_object_or_404(topic_service, param_name="topic_id")


@router.post(
    "/",
    response_model=ResponseBase[TopicOut],
    status_code=status.HTTP_201_CREATED,
    responses={
        201: common_response[201],
        404: common_response[404],
        500: common_response[500],
    },
    summary="Crear un nuevo tema",
)
async def create_topic(topic_create: TopicCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea un nuevo tema. Valida que el curso asociado exista.
    """
    # Se mantiene la validación para asegurar la integridad de los datos.
    course = await course_service.get(db=db, id=topic_create.course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El curso con id {topic_create.course_id} no existe.",
        )

    new_topic = await topic_service.create(db=db, obj_in=topic_create)
    topic_out = TopicOut.model_validate(new_topic)
    return create_response(
        data=[topic_out],
        message="Tema creado con éxito",
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/",
    response_model=ResponseBase[TopicOut],
    status_code=status.HTTP_200_OK,
    responses={200: common_response[200], 500: common_response[500]},
    summary="Obtener temas (con filtro opcional por curso)",
)
async def get_topics(
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1, description="Número de página"),
    limit: int = Query(default=10, ge=1, le=100, description="Temas por página"),
    course_id: Optional[int] = Query(
        default=None, description="Filtrar temas por ID de curso"
    ),
):
    """
    Obtiene una lista paginada de temas.
    - Si se provee course_id, filtra los temas para ese curso.
    - No carga relaciones para mantener la consulta ligera y rápida.
    """
    skip = (page - 1) * limit

    topics_db = await topic_service.get_multi(
        db, skip=skip, limit=limit, course_id=course_id
    )

    topics_out = [TopicOut.model_validate(t, from_attributes=True) for t in topics_db]

    return create_response(data=topics_out, message="Temas obtenidos con éxito")


@router.get(
    "/{topic_id}",
    response_model=ResponseBase[TopicOut],
    status_code=status.HTTP_200_OK,
    responses={404: common_response[404], 500: common_response[500]},
    summary="Obtener un tema por ID",
)
async def get_topic(topic: Topic = Depends(get_topic_or_404)):
    """
    Obtiene un tema por su ID. La dependencia maneja el error 404.
    """
    topic_out = TopicOut.model_validate(topic)
    return create_response(data=[topic_out], message="Tema obtenido con éxito")


@router.put(
    "/{topic_id}",
    response_model=ResponseBase[TopicOut],
    status_code=status.HTTP_200_OK,
    responses={404: common_response[404], 500: common_response[500]},
    summary="Actualizar un tema por ID",
)
async def update_topic(
    topic_update: TopicUpdate,
    topic_to_update: Topic = Depends(get_topic_or_404),
    db: AsyncSession = Depends(get_db),
):
    """
    Actualiza un tema. La dependencia y la validación manual aseguran
    que tanto el tema como el curso (si se cambia) existan.
    """
    if topic_update.course_id is not None:
        course = await course_service.get(db=db, id=topic_update.course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El curso con id {topic_update.course_id} no existe.",
            )

    updated_topic = await topic_service.update(
        db=db, db_obj=topic_to_update, obj_in=topic_update
    )
    topic_out = TopicOut.model_validate(updated_topic)
    return create_response(data=[topic_out], message="Tema actualizado con éxito")


@router.delete(
    "/{topic_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: common_response[404], 500: common_response[500]},
    summary="Eliminar un tema por ID",
)
async def delete_topic(
    topic_to_delete: Topic = Depends(get_topic_or_404),
    db: AsyncSession = Depends(get_db),
):
    """
    Elimina un tema. La dependencia se encarga de verificar si el tema existe.
    """
    await topic_service.remove(db=db, id=topic_to_delete.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
