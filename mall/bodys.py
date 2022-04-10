from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")
D = TypeVar("D")


class BaseBody(BaseModel):
    class Config:
        anystr_strip_whitespace = True


class Total(GenericModel, Generic[D]):
    total: int
    items: Optional[D]


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class Response(GenericModel, Generic[DataT]):
    data: Optional[DataT]
    errmsg: str = "ok"
    code: int = 200
