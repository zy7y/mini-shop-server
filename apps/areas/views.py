import json
from typing import List

from fastapi.encoders import jsonable_encoder

from apps.areas.bodys import AreaProvince, AreasInfo
from apps.areas.models import Area
from mall.bodys import Response
from mall.tools import area_redis


async def get_provinces() -> Response[List[AreaProvince]]:
    """获取省市区数据"""
    # 缓存中取
    if (provinces := await area_redis.get("provinces")) is not None:
        return Response(data=json.loads(provinces))
    # 省份数据
    provinces = await Area.filter(parent_id__isnull=True).all()

    # 缓存数据
    await area_redis.setex(
        "provinces", 15 * 60, json.dumps(jsonable_encoder(provinces))
    )
    return Response(data=provinces)


async def get_sub_areas(pk: int) -> Response[AreasInfo]:
    """查询市，或者区数据
    :params pk: 市 / 区 ID， int类型
    """
    cache_key = f"sub_{pk}"
    # 缓存中取
    data = await area_redis.get(cache_key)
    if data is not None:
        return Response(data=json.loads(data))

    current = await Area.get_or_none(id=pk)
    if current is not None:
        data = {
            **jsonable_encoder(current),
            "subs": jsonable_encoder(await Area.filter(parent=current).all()),
        }
        await area_redis.setex(cache_key, 15 * 60, json.dumps(data))
        return Response(data=data)
    return Response(code=400, errmsg="市或区数据错误")
