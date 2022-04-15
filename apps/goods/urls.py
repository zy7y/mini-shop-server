from typing import List

from fastapi.routing import APIRoute

from apps.goods.bodys import (DetailGoods, EsSearch, GoodsIndex, GoodsList,
                              GoodsListInfo)
from apps.goods.views import (detail_goods, get_history, goods_channel,
                              goods_list, hot_goods, save_history,
                              search_goods, visit_goods)
from mall.bodys import Response

urlpatterns = [
    APIRoute(
        "/index",
        goods_channel,
        summary="获取首页商品及广告数据",
        response_model=Response[GoodsIndex],
        tags=["商品"],
    ),
    APIRoute(
        "/list/{category_id}",
        goods_list,
        summary="查询列表页及排序",
        response_model=Response[GoodsList],
        tags=["商品"],
    ),
    APIRoute(
        "/host/{category_id}",
        hot_goods,
        summary="热销排行",
        response_model=Response[List[GoodsListInfo]],
        tags=["商品"],
    ),
    APIRoute(
        "/search",
        search_goods,
        summary="商品搜索",
        tags=["商品"],
        response_model=Response[EsSearch],
    ),
    APIRoute(
        "/detail/{sku_id}",
        detail_goods,
        summary="商品详情",
        tags=["商品"],
        response_model=Response[DetailGoods],
    ),
    APIRoute(
        "/detail/visit/{sku_id}",
        visit_goods,
        summary="统计分类商品访问量",
        tags=["商品"],
        response_model=Response,
    ),
    APIRoute(
        "/browse_histories",
        save_history,
        methods=["post"],
        summary="保存访问记录",
        tags=["商品"],
        response_model=Response,
    ),
    APIRoute(
        "/browse_histories",
        get_history,
        summary="查询访问记录",
        tags=["商品"],
        response_model=Response[List[GoodsListInfo]],
    ),
]
