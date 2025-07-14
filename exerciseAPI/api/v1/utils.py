from typing import List, Optional, TypeVar

from fastapi import status

from exerciseAPI.schemas.response import ResponseBase

T = TypeVar("T")


def create_response(
    data: Optional[List[T]] = None,
    message: str = "Operación exitosa",
    status_code: int = status.HTTP_200_OK,
    success: bool = True,
) -> ResponseBase[T]:
    return ResponseBase(
        status_code=status_code, message=message, success=success, results=data
    )
