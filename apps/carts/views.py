from decimal import Decimal

from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from apps.carts.bodys import CartCreate
from apps.goods.models import SKU
from apps.user.models import User
from mall.bodys import Response
from mall.security import check_token_http
from mall.tools import cart_redis


async def add_cart(cart: CartCreate, user: User = Depends(check_token_http)):
    """添加购物车"""
    sku = await SKU.get_or_none(pk=cart.sku_id)
    if sku is None:
        return Response(code=400, errmsg="商品不存在")

    redis_key = f"carts_{user.pk}"
    async with cart_redis.pipeline(transaction=True) as pipe:
        await pipe.hincrby(redis_key, cart.sku_id, cart.count).execute()
    return Response()


async def get_cart(user: User = Depends(check_token_http)):
    """获取购物车"""
    redis_key = f"carts_{user.pk}"
    cart = await cart_redis.hgetall(redis_key)
    data = []
    for sku_id, count in cart.items():
        sku = await SKU.get_or_none(pk=sku_id)
        data.append(
            {
                **jsonable_encoder(sku),
                "count": count,
                "amount": sku.price * Decimal(count),
            }
        )
    return Response(data=data)


async def put_cart(cart: CartCreate, user: User = Depends(check_token_http)):

    sku = await SKU.get_or_none(pk=cart.sku_id)
    if sku is None:
        return Response(code=400, errmsg="商品不存在")

    redis_key = f"carts_{user.pk}"
    async with cart_redis.pipeline(transaction=True) as pipe:
        # 覆盖原有数据
        await pipe.hset(redis_key, cart.sku_id, cart.count).execute()

    return Response(
        data={
            **sku,
            "count": cart.count,
            "amount": sku.price * Decimal(cart.count),
        }
    )


async def del_cart(sku_id: int, user: User = Depends(check_token_http)):
    sku = await SKU.get_or_none(pk=sku_id)
    if sku is None:
        return Response(code=400, errmsg="商品不存在")
    redis_key = f"carts_{user.pk}"
    await cart_redis.hdel(redis_key, sku_id)
    return Response()
