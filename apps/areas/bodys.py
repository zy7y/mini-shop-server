from typing import List

from pydantic import BaseModel, Field


class AreasBase(BaseModel):
    id: int = Field(..., description="ID")
    name: str = Field(..., description="名字")


class AreaProvince(AreasBase):
    """省数据"""

    pass


class AreasInfo(AreasBase):
    subs: List[AreasBase] = Field(..., description="子级")
