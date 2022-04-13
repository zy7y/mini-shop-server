from typing import List

from fastapi.routing import APIRoute

from apps.goods.bodys import GoodsIndex, GoodsList, GoodsListInfo
from apps.goods.views import goods_channel, goods_list, hot_goods
from mall.bodys import Response

urlpatterns = [
    APIRoute(
        "/index",
        goods_channel,
        summary="获取首页商品及广告数据",
        response_model=Response[GoodsIndex],
    ),
    APIRoute(
        "/list/{category_id}",
        goods_list,
        summary="查询列表页及排序",
        response_model=Response[GoodsList],
    ),
    APIRoute(
        "/host/{category_id}",
        hot_goods,
        summary="热销排行",
        response_model=Response[List[GoodsListInfo]],
    ),
]
