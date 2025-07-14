from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from exerciseAPI.api.v1.dependencies import get_object_or_404
from exerciseAPI.api.v1.utils import create_response
from exerciseAPI.core.database import get_db
from exerciseAPI.models import Topic
from exerciseAPI.schemas.response import ResponseBase
from exerciseAPI.schemas.topic import TopicCreate, TopicOut, TopicUpdate
from exerciseAPI.services.course_service import course_service
from exerciseAPI.services.topic_service import topic_service

router = APIRouter()


get_topic_or_404 = get_object_or_404(topic_service)


@router.post(
    "/",
    response_model=ResponseBase[TopicOut],
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo tema",
)
async def create_topic(topic_create: TopicCreate, db: AsyncSession = Depends(get_db)):
    """
    Crea un nuevo tema asociado a un curso.

    - **Valida** que el curso (`course_id`) exista.
    - **Crea** el tema de forma asíncrona.
    - **Retorna** el tema recién creado.
    """
    course = await course_service.get(db=db, id=topic_create.course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El curso con id {topic_create.course_id} no existe.",
        )

    new_topic = await topic_service.create(db=db, obj_in=topic_create)
    topic_out = TopicOut.model_validate(new_topic, from_attributes=True)

    return create_response(
        data=[topic_out],
        message="Tema creado con éxito",
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/",
    response_model=ResponseBase[TopicOut],
    summary="Obtener temas (con filtro opcional por curso)",
)
async def get_topics(
    db: AsyncSession = Depends(get_db),
    course_id: Optional[int] = Query(
        default=None, description="Filtrar temas por ID de curso"
    ),
):
    """
    Obtiene una lista de temas.

    - Si se provee `course_id`, filtra los temas para ese curso.
    - De lo contrario, devuelve todos los temas.
    """
    if course_id is not None:
        topics_orm = await topic_service.get_multi_by_course(db, course_id=course_id)
    else:
        topics_orm = await topic_service.get_multi(db, limit=100)

    topics_out = [TopicOut.model_validate(t, from_attributes=True) for t in topics_orm]
    return create_response(data=topics_out, message="Temas obtenidos con éxito")


@router.get(
    "/{topic_id}",
    response_model=ResponseBase[TopicOut],
    summary="Obtener un tema por ID",
)
async def get_topic(topic: Topic = Depends(get_topic_or_404)):
    """
    Obtiene un único tema por su ID usando la dependencia.
    """
    topic_out = TopicOut.model_validate(topic, from_attributes=True)
    return create_response(data=[topic_out], message="Tema obtenido con éxito")


@router.put(
    "/{topic_id}",
    response_model=ResponseBase[TopicOut],
    summary="Actualizar un tema por ID",
)
async def update_topic(
    topic_update: TopicUpdate,
    topic_to_update: Topic = Depends(get_topic_or_404),
    db: AsyncSession = Depends(get_db),
):
    """
    Actualiza la información de un tema existente de forma asíncrona.
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
    topic_out = TopicOut.model_validate(updated_topic, from_attributes=True)
    return create_response(data=[topic_out], message="Tema actualizado con éxito")


@router.delete(
    "/{topic_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un tema por ID",
)
async def delete_topic(
    topic_to_delete: Topic = Depends(get_topic_or_404),
    db: AsyncSession = Depends(get_db),
):
    """
    Elimina un tema de la base de datos de forma asíncrona.
    """
    await topic_service.remove(db=db, id=topic_to_delete.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
