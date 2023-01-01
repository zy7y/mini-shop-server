from typing import Generic, TypeVar, Optional, List

from ninja import Schema
from pydantic import generics, Field

T = TypeVar('T')


class R(generics.GenericModel, Generic[T]):
    code: int = 1
    data: Optional[T]
    msg: str = "ok"

    @classmethod
    def ok(cls, data: T = None) -> "R":
        return cls(code=1, data=data, msg="ok")

    @classmethod
    def fail(cls, msg: str = "fail") -> "R":
        return cls(code=0, msg=msg)


class Token(Schema):
    token: str


class PageParams(Schema):
    limit: int = Field(10, ge=1, description="每页数量")
    offset: int = Field(1, ge=1)


class PageResult(generics.GenericModel, Generic[T]):
    count: int = 0
    items: List[T] = None
