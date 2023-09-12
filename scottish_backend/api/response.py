from typing import Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    status_code: int
    error: bool
    data: T | None = Field(default=None)
    msg: dict[int | str, str] | None = Field(default=None)
