from collections import OrderedDict
from typing import Optional

from fastapi import Query

from apps.contents.models import Content, ContentCategory
from apps.goods.models import SKU, GoodsCategory, GoodsChannel
from mall.bodys import Response


async def goods_channel():
    """商品频道分类-首页"""
    categories = OrderedDict()
    channels = await GoodsChannel.all().order_by("group_id", "sequence")
    for channel in channels:
        group_id = channel.group_id
        if group_id not in categories:
            categories[group_id] = {"channels": [], "sub_cats": []}
        # 当前频道的类别
        cat1 = await GoodsCategory.get(pk=channel.category_id)

        # 追加当前频道
        categories[group_id]["channels"].append(
            {"id": cat1.pk, "name": cat1.name, "url": channel.url}
        )

        for cat2 in await cat1.subs.all():
            cat2.sub_cats = []
            for cat3 in await cat2.subs.all():
                cat2.sub_cats.append({"id": cat3.pk, "name": cat3.name})
            categories[group_id]["sub_cats"].append(
                {"id": cat2.pk, "name": cat2.name, "sub_cats": cat2.sub_cats}
            )
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
    category = await GoodsCategory.get_or_none(pk=category_id)
    if category is None:
        return Response(code=400, errmsg="分类数据错误")

    # 查询面包屑导航
    breadcrumb = dict(cat1="", cat2="", cat3="")
    if category.parent_id is None:
        # 当前类别为一级类别
        breadcrumb["cat1"] = category.name
    elif await GoodsCategory.filter(parent_id=category_id).count() == 0:
        # 当前类别为三级
        breadcrumb["cat3"] = category.name
        breadcrumb.update(
            await GoodsCategory.get(id=category.parent_id).values(cat2="name")
        )
        breadcrumb.update(
            await GoodsCategory.get(
                id=(await GoodsCategory.get(id=category.parent_id)).parent_id
            ).values(cat1="name")
        )
    else:
        # 当前类别为二级
        breadcrumb["cat2"] = category.name
        breadcrumb.update(
            await GoodsCategory.get(id=category.parent_id).values(cat1="name")
        )

    # 排序 & 分页
    try:
        if ordering is None:
            ordering = "-id"
        total = await SKU.all().count()
        skus = (
            await SKU.filter(category=category, is_launched=True)
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
