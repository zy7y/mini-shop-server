from typing import Optional

from pydantic import Field
from pydantic.types import Decimal

from apps.goods.bodys import GoodsListInfo
from mall.bodys import BaseBody


class CartCreate(BaseBody):
    sku_id: int
    count: int = Field(..., description="商品数量", gt=0)


class CartSKU(GoodsListInfo):
    count: int = Field(..., description="加购数量")
    amount: Optional[Decimal] = Field(None, description="总价")
