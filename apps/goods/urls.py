from typing import List

from fastapi.routing import APIRoute

from apps.goods.bodys import GoodsIndex, GoodsList, GoodsListInfo, EsSearch
from apps.goods.views import goods_channel, goods_list, hot_goods, search_goods
from mall.bodys import Response

urlpatterns = [
    APIRoute(
        "/index",
        goods_channel,
        summary="获取首页商品及广告数据",
        response_model=Response[GoodsIndex],
        tags=["商品"]
    ),
    APIRoute(
        "/list/{category_id}",
        goods_list,
        summary="查询列表页及排序",
        response_model=Response[GoodsList],
        tags=["商品"]
    ),
    APIRoute(
        "/host/{category_id}",
        hot_goods,
        summary="热销排行",
        response_model=Response[List[GoodsListInfo]],
        tags=["商品"]
    ),
    APIRoute(
        "/search",
        search_goods,
        summary="商品搜索",
        tags=["商品"],
        response_model=Response[EsSearch]
    ),
]
