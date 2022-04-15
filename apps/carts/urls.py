from typing import List

from fastapi.routing import APIRoute

from apps.carts.bodys import CartSKU
from apps.carts.views import add_cart, del_cart, get_cart, put_cart
from mall.bodys import Response

urlpatterns = [
    APIRoute(
        "/cart",
        add_cart,
        methods=["post"],
        summary="添加购物车",
        tags=["购物车"],
        response_model=Response,
    ),
    APIRoute(
        "/cart",
        get_cart,
        summary="查购物车",
        tags=["购物车"],
        response_model=Response[List[CartSKU]],
    ),
    APIRoute(
        "/cart",
        put_cart,
        methods=["put"],
        summary="修改购物车",
        tags=["购物车"],
        response_model=Response[CartSKU],
    ),
    APIRoute(
        "/cart/{sku_id}",
        del_cart,
        methods=["delete"],
        summary="删除购物车",
        tags=["购物车"],
        response_model=Response,
    ),
]
