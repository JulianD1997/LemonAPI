# exerciseAPI/api/v1/endpoints/modules.py

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from exerciseAPI.api.v1.dependencies import get_object_or_404
from exerciseAPI.api.v1.utils import create_response
from exerciseAPI.core.database import get_db
from exerciseAPI.models import Module
from exerciseAPI.schemas.module import ModuleCreate, ModuleOut, ModuleUpdate
from exerciseAPI.schemas.response import ResponseBase, common_response
from exerciseAPI.services.course_service import course_service
from exerciseAPI.services.module_service import module_service

router = APIRouter()

get_module_or_404 = get_object_or_404(module_service, param_name="module_id")


@router.post(
    "/",
    response_model=ResponseBase[ModuleOut],
    status_code=status.HTTP_201_CREATED,
    responses={
        201: common_response[201],
        404: common_response[404],
        400: common_response[400],
        500: common_response[500],
    },
    summary="Crear un nuevo módulo",
)
async def create_module(
    module_create: ModuleCreate, db: AsyncSession = Depends(get_db)
):
    """
    Crea un nuevo módulo asociado a un curso.

    - **Valida** que el curso (`course_id`) exista.
    - **Crea** el módulo de forma asíncrona.
    - **Retorna** el módulo recién creado.
    """
    course = await course_service.get(db=db, id=module_create.course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El curso con id {module_create.course_id} no existe.",
        )

    new_module = await module_service.create(db=db, obj_in=module_create)
    module_out = ModuleOut.model_validate(new_module, from_attributes=True)
    return create_response(
        data=[module_out],
        message="Módulo creado con éxito",
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/",
    response_model=ResponseBase[ModuleOut],
    status_code=status.HTTP_200_OK,
    responses={200: common_response[200], 500: common_response[500]},
    summary="Obtener módulos (con filtro opcional por curso)",
)
async def get_modules(
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1, description="Número de página"),
    limit: int = Query(default=10, ge=1, le=100, description="Módulos por página"),
    course_id: Optional[int] = Query(
        default=None, description="Filtrar módulos por ID de curso"
    ),
):
    """
    Obtiene una lista paginada de módulos.
    - Si se provee `course_id`, filtra los módulos para ese curso.
    """
    skip = (page - 1) * limit

    modules_orm = await module_service.get_multi(
        db, skip=skip, limit=limit, course_id=course_id
    )

    if not modules_orm:
        message = "No se encontraron módulos."
        if course_id:
            message = f"No se encontraron módulos para el curso con ID {course_id}."
    else:
        message = "Módulos obtenidos con éxito."

    modules_out = [
        ModuleOut.model_validate(mod, from_attributes=True) for mod in modules_orm
    ]

    return create_response(data=modules_out, message=message)


@router.get(
    "/{module_id}",
    response_model=ResponseBase[ModuleOut],
    status_code=status.HTTP_200_OK,
    responses={404: common_response[404], 500: common_response[500]},
    summary="Obtener un módulo por ID",
)
async def get_module(module: Module = Depends(get_module_or_404)):
    """
    Obtiene un único módulo por su ID. La dependencia maneja el error 404.
    """
    module_out = ModuleOut.model_validate(module, from_attributes=True)
    return create_response(data=[module_out], message="Módulo obtenido con éxito")


@router.put(
    "/{module_id}",
    response_model=ResponseBase[ModuleOut],
    status_code=status.HTTP_200_OK,
    responses={
        200: common_response[200],
        404: common_response[404],
        500: common_response[500],
    },
    summary="Actualizar un módulo por ID",
)
async def update_module(
    module_update: ModuleUpdate,
    module_to_update: Module = Depends(get_module_or_404),
    db: AsyncSession = Depends(get_db),
):
    """
    Actualiza la información de un módulo existente.
    - **Valida** que el curso (`course_id`) exista si se proporciona.
    """
    if module_update.course_id:
        course = await course_service.get(db=db, id=module_update.course_id)
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El curso con id {module_update.course_id} no existe.",
            )

    updated_module = await module_service.update(
        db=db, db_obj=module_to_update, obj_in=module_update
    )
    module_out = ModuleOut.model_validate(updated_module, from_attributes=True)
    return create_response(data=[module_out], message="Módulo actualizado con éxito")


@router.delete(
    "/{module_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: common_response[404], 500: common_response[500]},
    summary="Eliminar un módulo por ID",
)
async def delete_module(
    module_to_delete: Module = Depends(get_module_or_404),
    db: AsyncSession = Depends(get_db),
):
    """
    Elimina un módulo de la base de datos.
    """
    await module_service.remove(db=db, id=module_to_delete.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
