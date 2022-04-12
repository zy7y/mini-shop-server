from typing import List

from fastapi.routing import APIRoute

from apps.areas.bodys import AreaProvince, AreasInfo
from apps.areas.views import get_provinces, get_sub_areas
from mall.bodys import Response

urlpatterns = [
    APIRoute(
        "/areas",
        get_provinces,
        summary="获取省数据",
        response_model=Response[List[AreaProvince]],
        tags=["公共服务"],
    ),
    APIRoute(
        "/areas/{id}",
        get_sub_areas,
        summary="获取市/区数据",
        response_model=Response[AreasInfo],
        tags=["公共服务"],
    ),
]
