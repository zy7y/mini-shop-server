from fresh_mall.model import BaseModel, fields


class OrderInfo(BaseModel):

    PAY_METHODS = {"1": "货到付款", "2": "微信支付", "3": "支付宝", "4": "银联支付"}

    PAY_METHODS_ENUM = {"CASH": 1, "ALIPAY": 2}

    ORDER_STATUS_ENUM = {
        "UNPAID": 1,
        "UNSEND": 2,
        "UNRECEIVED": 3,
        "UNCOMMENT": 4,
        "FINISHED": 5,
    }
    PAY_METHOD_CHOICES = ((1, "货到付款"), (2, "微信支付"), (3, "支付宝"), (4, "银联支付"))

    ORDER_STATUS = {1: "待支付", 2: "待发货", 3: "待收货", 4: "待评价", 5: "已完成"}

    ORDER_STATUS_CHOICES = ((1, "待支付"), (2, "待发货"), (3, "待收货"), (4, "待评价"), (5, "已完成"))

    order_id = fields.CharField(max_length=128, pk=True, description="订单ID")
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    addr = fields.ForeignKeyField("models.Address", on_delete=fields.CASCADE)
    pay_method = fields.SmallIntField(default=3, description=str(PAY_METHOD_CHOICES))
    total_count = fields.IntField(default=1, description="商品数量")
    total_price = fields.DecimalField(max_digits=10, decimal_places=2, description="商品总价")
    transit_price = fields.DecimalField(max_digits=10, decimal_places=2, description="订单运费")
    order_status = fields.SmallIntField(default=1, description=str(ORDER_STATUS_CHOICES) + "订单状态")
    trade_no = fields.CharField(max_length=128, default="", description="支付编号")

    class Meta:
        table = "fm_order_info"
        table_description = "订单详细"


class OrderGoods(BaseModel):
    order = fields.ForeignKeyField("models.OrderInfo", on_delete=fields.RESTRICT)
    sku = fields.ForeignKeyField("models.GoodsSKU", on_delete=fields.RESTRICT)
    count = fields.IntField(default=1, description="商品数量")
    price = fields.DecimalField(max_digits=10, decimal_places=2, description="商品单价")
    comment = fields.CharField(max_length=256, default="", description="评论")

    class Meta:
        table = "fm_order_goods"
        table_description = "订单商品"
