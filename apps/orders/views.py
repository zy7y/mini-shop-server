from datetime import datetime
from decimal import Decimal

from fastapi import Depends

from apps.goods.models import SKU
from apps.orders.bodys import OrderBody
from apps.orders.models import OrderGoods, OrderInfo
from apps.user.models import Address, User
from mall.bodys import Response
from mall.security import check_token_http
from mall.tools import cart_redis


async def create_order(order: OrderBody, user: User = Depends(check_token_http)):
    """创建订单"""
    address = await Address.get_or_none(pk=order.address_id)
    if address is None:
        return Response(code=400, errmsg="地址错误")
    # 创建编号ID
    order_id = datetime.now().strftime("%Y%m%d%H%M%S") + ("%09d" % user.id)
    order_info = await OrderInfo.create(
        order_id=order_id,
        user_id=user.pk,
        address_id=address.pk,
        total_count=0,
        total_amount=Decimal("0"),
        freight=Decimal("10.00"),
        pay_method=order.pay_method,
        status=OrderInfo.ORDER_STATUS_ENUM["UNPAID"]
        if order.pay_method == OrderInfo.PAY_METHODS_ENUM["ALIPAY"]
        else OrderInfo.ORDER_STATUS_ENUM["UNSEND"],
    )

    # 保存商品订单信息
    redis_key = f"carts_{user.pk}"
    carts = await cart_redis.hgetall(redis_key)
    if not carts:
        return Response(code=400, errmsg="无商品订单")

    for sku_id, count in carts.items():
        sku = await SKU.get(pk=sku_id)
        count = int(count)
        # 判断库存
        if count < sku.stock:
            return Response(code=400, errmsg="库存不足")

        # 修改销量和库存
        sku.stock -= count
        sku.sales += count
        await sku.save()

        # 保存商品订单信息
        await OrderGoods.create(
            order_id=order_info.order_id, sku_id=sku.pk, count=count, price=sku.price
        )

        order_info.total_count += count
        order_info.total_amount += count * sku.price

    # 添加邮费
    order_info.total_amount += order_info.freight
    await order_info.save()

    # 清除购物车数据
    await cart_redis.delete(redis_key)
    return Response(data={"order_id": order_info.order_id})
