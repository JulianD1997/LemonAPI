from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from exerciseAPI.api.v1.dependencies import get_object_or_404
from exerciseAPI.api.v1.utils import create_response
from exerciseAPI.core.database import get_db
from exerciseAPI.models import Course
from exerciseAPI.schemas.course import CourseCreate, CourseOut, CourseUpdate
from exerciseAPI.schemas.response import ResponseBase, common_response
from exerciseAPI.services.course_service import course_service

router = APIRouter()
get_course_or_404 = get_object_or_404(course_service, param_name="course_id")


@router.post(
    "/",
    response_model=ResponseBase[CourseOut],
    status_code=status.HTTP_201_CREATED,
    responses={201: common_response[201], 500: common_response[500]},
    summary="Crear un nuevo curso",
)
async def create_course(
    course_create: CourseCreate, db: AsyncSession = Depends(get_db)
):
    """
    Crea un nuevo curso en la base de datos.
    """
    new_course = await course_service.create(db=db, obj_in=course_create)
    course_out = CourseOut.model_validate(new_course)
    return create_response(
        data=[course_out],
        message="Curso creado con éxito",
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/",
    response_model=ResponseBase[CourseOut],
    status_code=status.HTTP_200_OK,
    responses={200: common_response[200], 500: common_response[500]},
    summary="Obtener todos los cursos",
)
async def get_courses(
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1, description="Número de página"),
    limit: int = Query(default=10, ge=1, le=100, description="Cursos por página"),
):
    """
    Obtiene una lista paginada de cursos. No carga relaciones por defecto.
    """
    skip = (page - 1) * limit
    courses_db = await course_service.get_multi(db, skip=skip, limit=limit)
    courses_out = []

    for c in courses_db:
        try:
            courses_out.append(CourseOut.model_validate(c, from_attributes=True))
        except Exception as e:
            print(f"Error validando el curso {c}: {e}")

    print(courses_out)

    return create_response(data=courses_out, message="Cursos obtenidos con éxito")


@router.get(
    "/{course_id}",
    response_model=ResponseBase[CourseOut],
    status_code=status.HTTP_200_OK,
    responses={404: common_response[404], 500: common_response[500]},
    summary="Obtener un curso por ID",
)
async def get_course(
    course: Course = Depends(get_course_or_404),
):
    """
    Obtiene un curso específico por su ID.
    Si el curso no existe, devuelve un error 404.
    """
    course_out = CourseOut.model_validate(course)
    return create_response(data=[course_out], message="Curso obtenido con éxito")


@router.put(
    "/{course_id}",
    response_model=ResponseBase[CourseOut],
    status_code=status.HTTP_200_OK,
    responses={404: common_response[404], 500: common_response[500]},
    summary="Actualizar un curso por ID",
)
async def update_course(
    course_update: CourseUpdate,
    course_to_update: Course = Depends(get_course_or_404),
    db: AsyncSession = Depends(get_db),
):
    """
    Actualiza un curso existente.
    Primero busca el curso y si no lo encuentra, devuelve un 404.
    """
    updated_course = await course_service.update(
        db=db, db_obj=course_to_update, obj_in=course_update
    )
    course_out = CourseOut.model_validate(updated_course)
    return create_response(data=[course_out], message="Curso actualizado con éxito")


@router.delete(
    "/{course_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: common_response[404], 500: common_response[500]},
    summary="Eliminar un curso por ID",
)
async def delete_course(
    course_to_delete: Course = Depends(get_course_or_404),
    db: AsyncSession = Depends(get_db),
):
    """
    Elimina un curso de la base de datos.
    La dependencia se encarga de verificar si el curso existe.
    """
    await course_service.remove(db=db, id=course_to_delete.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
