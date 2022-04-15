from collections import OrderedDict

from apps.goods.models import GoodsCategory, GoodsChannel


async def find_goods_category():
    """查询商品频道分类"""
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
    return categories


async def find_breadcrumb(category_id: int):
    """查询面包屑导航
    :params category_id: 分类ID
    """

    category = await GoodsCategory.get_or_none(pk=category_id)
    if category is None:
        return None

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
    return breadcrumb
