from apps.areas.views import get_provinces, get_sub_areas
from mall.router import Route as APIRoute

urlpatterns = [
    APIRoute(
        "/areas",
        get_provinces,
        summary="获取省数据",
        tags=["公共服务"],
    ),
    APIRoute(
        "/areas/{id}",
        get_sub_areas,
        summary="获取市/区数据",
        tags=["公共服务"],
    ),
]
