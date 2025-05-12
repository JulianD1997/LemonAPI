from typing import Generic, List, Optional, TypeVar

from pydantic.generics import GenericModel

T = TypeVar("T")


class ResponseBase(GenericModel, Generic[T]):
    status_code: int
    message: str
    success: bool
    results: Optional[List[T]] | None = None
