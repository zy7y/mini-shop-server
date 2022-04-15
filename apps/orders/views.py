from datetime import datetime
from decimal import Decimal

from fastapi import Depends
from tortoise.exceptions import OperationalError
from tortoise.transactions import atomic

from apps.goods.models import SKU
from apps.orders.bodys import OrderBody
from apps.orders.models import OrderGoods, OrderInfo
from apps.user.models import Address, User
from mall.bodys import Response
from mall.security import check_token_http
from mall.tools import cart_redis


async def create_order(order: OrderBody, user: User = Depends(check_token_http)):
    """创建订单"""
    redis_key = f"carts_{user.pk}"

    address = await Address.get_or_none(pk=order.address_id)
    if address is None:
        return Response(code=400, errmsg="地址错误")
    # 创建编号ID
    order_id = datetime.now().strftime("%Y%m%d%H%M%S") + ("%09d" % user.id)

    @atomic()
    async def create_data_tran():
        """创建订单事务"""
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

        carts = await cart_redis.hgetall(redis_key)
        if not carts:
            return Response(code=400, errmsg="无商品订单")

        for sku_id, count in carts.items():
            # 乐观锁
            while True:
                sku = await SKU.get(pk=sku_id)
                count = int(count)

                origin_stock = sku.stock
                origin_sales = sku.sales

                # 判断库存
                if count < sku.stock:
                    return Response(code=400, errmsg="库存不足")

                new_stock = origin_stock - count
                new_sales = origin_sales + count
                result = await SKU.filter(pk=sku.pk, stock=origin_stock).update(
                    stock=new_stock, sales=new_sales
                )

                # 没修改数据
                if result == 0:
                    continue

                # 保存商品订单信息
                await OrderGoods.create(
                    order_id=order_info.order_id,
                    sku_id=sku.pk,
                    count=count,
                    price=sku.price,
                )

                order_info.total_count += count
                order_info.total_amount += count * sku.price

                break
        # 添加邮费
        order_info.total_amount += order_info.freight
        await order_info.save()

    try:
        await create_data_tran()
    except OperationalError:
        return Response(code=400, errmsg="下单失败")

    # 清除购物车数据
    await cart_redis.delete(redis_key)
    return Response(data={"order_id": order_id})
