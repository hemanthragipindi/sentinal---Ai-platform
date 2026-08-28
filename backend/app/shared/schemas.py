from typing import Any, Generic, TypeVar
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: T | None = None
    meta: dict[str, Any] | None = None
    
    model_config = ConfigDict(from_attributes=True)

class PaginatedMeta(BaseModel):
    total: int
    page: int
    size: int
    pages: int

class PaginatedResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: list[T]
    meta: PaginatedMeta
    
    model_config = ConfigDict(from_attributes=True)

def success_response(data: Any = None, message: str = "Operation completed successfully.", meta: dict[str, Any] | None = None) -> StandardResponse:
    return StandardResponse(success=True, message=message, data=data, meta=meta)

def error_response(message: str, data: Any = None, meta: dict[str, Any] | None = None) -> StandardResponse:
    return StandardResponse(success=False, message=message, data=data, meta=meta)
