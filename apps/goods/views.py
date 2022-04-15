from collections import OrderedDict
from typing import Any, Optional

from fastapi import Depends, Query

from apps.contents.models import Content, ContentCategory
from apps.goods.bodys import SkuHistory
from apps.goods.models import SKU, GoodsCategory, GoodsChannel
from apps.goods.search_es import query_es
from apps.goods.utils import find_breadcrumb, find_goods_category
from apps.user.models import User
from mall.bodys import Response
from mall.security import check_token_http
from mall.tools import history_redis


async def goods_channel():
    """商品频道分类-首页"""
    categories = await find_goods_category()
    # 广告数据
    contents = {}
    for cat in await ContentCategory.all():
        items = (
            await Content.filter(category_id=cat.pk, status=True)
            .order_by("sequence")
            .all()
            .values(
                "id",
                "title",
                "url",
                "image",
                "text",
                "sequence",
                category="category__name",
            )
        )
        contents[cat.key] = items

    return Response(data={"categories": categories, "contents": contents})


async def goods_list(
    category_id: int,
    page: int = Query(default=1, description="页码", gte=1),
    page_size: int = Query(default=5, description="页码", gte=5),
    ordering: Optional[str] = None,
):
    """查询列表分页和排序"""
    # 查询面包屑导航
    breadcrumb = await find_breadcrumb(category_id)
    if breadcrumb is None:
        return Response(code=400, errmsg="分类不存在")
    # 排序 & 分页
    try:
        if ordering is None:
            ordering = "-id"
        total = await SKU.all().count()
        skus = (
            await SKU.filter(category=category_id, is_launched=True)
            .order_by(ordering)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
    except Exception as e:
        return Response(code=400, errmsg=str(e))

    return Response(data={"count": total, "list": skus, "breadcrumb": breadcrumb})


async def hot_goods(category_id: int):
    """商品热销排行"""
    return Response(
        data=await SKU.filter(category_id=category_id, is_launched=True)
        .order_by("-sales")
        .limit(2)
    )


async def search_goods(
    q: Any = Query(..., description="查询sku名称 或者副标题的数据"),
    page: int = Query(default=1, description="页数"),
    page_size: int = Query(default=5, description="条数"),
):
    """商品搜索"""
    try:
        total, resp = await query_es(q, page, page_size)
        return Response(
            data={
                "info": {"count": total, "page_size": len(resp), "search_key": q},
                "goods": resp,
            }
        )
    except Exception as e:
        return Response(code=400, errmsg=str(e))


async def detail_goods(sku_id: int):
    """商品详情"""
    sku_obj = await SKU.get_or_none(pk=sku_id, is_launched=True, is_delete=False)
    if sku_obj is None:
        return Response(code=400, errmsg="商品不存在")
    # 查询商品频道分类
    categories = await find_goods_category()
    # 查询面包屑导航
    breadcrumb = await find_breadcrumb(sku_obj.category_id)
    return Response(
        data={
            "categories": categories,
            "breadcrumb": breadcrumb,
            "sku": sku_obj,
        }
    )


async def visit_goods(category_id: int):
    """分类商品访问量"""
    category = await GoodsCategory.get_or_none(pk=category_id)
    if category is None:
        return Response(code=400, errmsg="分类不存在")

    from datetime import date

    today = date.today()

    from apps.goods.models import GoodsVisitCount

    visit_obj = await GoodsVisitCount.get_or_none(category_id=category_id, date=today)
    if visit_obj is None:
        visit_obj = GoodsVisitCount(category_id=category_id, count=0, date=today)
    visit_obj.count += 1
    await visit_obj.save()
    return Response()


async def save_history(history: SkuHistory, user: User = Depends(check_token_http)):
    """保存用户浏览记录"""
    sku_id = history.sku_id
    sku = await SKU.get_or_none(pk=sku_id)
    if sku is None:
        return Response(code=400, errmsg="SKU不存在")

    redis_key = f"history_{user.pk}"

    async with history_redis.pipeline(transaction=True) as pipe:
        await pipe.lrem(redis_key, 0, sku_id).lpush(redis_key, sku_id).ltrim(
            redis_key, 0, 4
        ).execute()

    return Response()


async def get_history(user: User = Depends(check_token_http)):
    """查询用户浏览记录"""
    redis_key = f"history_{user.pk}"
    sku_ids = await history_redis.lrange(redis_key, 0, -1)
    return Response(data=[await SKU.get_or_none(pk=sku_id) for sku_id in sku_ids])
