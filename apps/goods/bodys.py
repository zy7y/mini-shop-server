from typing import Dict, List, Optional

from pydantic import BaseModel, validator


class GoodsChannelsBase(BaseModel):
    id: str
    name: str


class SubsChannels(GoodsChannelsBase):
    sub_cats: Optional[List["SubsChannels"]]


class Channels(GoodsChannelsBase):
    url: str
    sub_cats: Optional[List[SubsChannels]]


class Categories(BaseModel):
    channels: List[Channels]


class Content(BaseModel):
    id: int
    title: str
    url: str
    image: str
    text: str
    sequence: int
    category: str

    @validator("image")
    def build_image_url(cls, v: str):
        if v == "":
            return v
        return "https://49.232.203.244/" + v


class GoodsIndex(BaseModel):
    """首页商品及广告模型"""

    contents: Dict[str, List[Content]]
    categories: Dict[str, Categories]


class BuildImage(BaseModel):
    default_image: str

    @validator("default_image")
    def build_image_url(cls, v: str):
        if v == "":
            return v
        return "https://49.232.203.244/" + v


class BreadCrumb(BaseModel):
    """分页导航"""

    cat1: str
    cat2: str
    cat3: str


class GoodsListInfo(BuildImage):
    """列表商品页"""

    id: int
    name: str
    price: float


class GoodsList(BaseModel):
    count: int
    list: List[GoodsListInfo]
    breadcrumb: BreadCrumb


class EsSearchInfo(BaseModel):
    search_key: str
    page_size: int
    count: int


class EsSearch(BaseModel):
    info: EsSearchInfo
    goods: List[GoodsListInfo]


class DetailGoods(BaseModel):
    categories: Dict[str, Categories]
    breadcrumb: BreadCrumb
    sku: GoodsListInfo


class SkuHistory(BaseModel):
    sku_id: int
