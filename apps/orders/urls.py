from fastapi.routing import APIRoute

from apps.orders.views import create_order
from mall.bodys import Response

urlpatterns = [
    APIRoute(
        "/orders/commit",
        create_order,
        methods=["post"],
        tags=["订单"],
        summary="提交订单",
        response_model=Response,
    )
]
