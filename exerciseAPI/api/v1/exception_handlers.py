from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from exerciseAPI.api.v1.utils import create_response


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=create_response(
            message="Ocurrió un error inesperado en la base de datos.",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            success=False,
        ).model_dump(),  # .dict() está obsoleto, usamos .model_dump()
    )
