from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseBase(BaseModel, Generic[T]):
    status_code: int
    message: str
    success: bool
    results: Optional[List[T]] | None = None


common_response = {
    200: {
        "model": ResponseBase[None],
        "description": "Operación exitosa",
        "content": {
            "application/json": {
                "example": {
                    "status_code": 200,
                    "message": "Operación exitosa.",
                    "success": True,
                    "results": [],
                }
            }
        },
    },
    201: {
        "model": ResponseBase[None],
        "description": "Creado con éxito",
        "content": {
            "application/json": {
                "example": {
                    "status_code": 201,
                    "message": "Creado con éxito.",
                    "success": True,
                    "results": [],
                }
            }
        },
    },
    400: {
        "model": ResponseBase[None],
        "description": "Error de validación.",
        "content": {
            "application/json": {
                "example": {
                    "status_code": 400,
                    "message": "Error de validación.",
                    "success": False,
                    "results": [],
                }
            }
        },
    },
    404: {
        "model": ResponseBase[None],
        "description": "No encontrado.",
        "content": {
            "application/json": {
                "example": {
                    "status_code": 404,
                    "message": "No encontrado.",
                    "success": False,
                    "results": [],
                }
            }
        },
    },
    500: {
        "model": ResponseBase[None],
        "description": "Error interno del servidor",
        "content": {
            "application/json": {
                "example": {
                    "status_code": 500,
                    "message": "Error interno del servidor",
                    "success": False,
                    "results": None,
                }
            }
        },
    },
}
