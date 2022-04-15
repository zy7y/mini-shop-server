from tortoise import fields, models


class OrderInfo(models.Model):
    PAY_METHODS_ENUM = {"CASH": 1, "ALIPAY": 2}
    # 支付方式
    PAY_METHOD_CHOICES = (
        (1, "货到付款"),
        (2, "支付宝"),
    )
    ORDER_STATUS_ENUM = {
        "UNPAID": 1,
        "UNSEND": 2,
        "UNRECEIVED": 3,
        "UNCOMMENT": 4,
        "FINISHED": 5,
    }
    # 订单状态
    ORDER_STATUS_CHOICES = (
        (1, "待支付"),
        (2, "待发货"),
        (3, "待收货"),
        (4, "待评价"),
        (5, "已完成"),
        (6, "已取消"),
    )

    order_id = fields.CharField(max_length=64, pk=True, description="订单号")
    user = fields.ForeignKeyField(
        "models.User", on_delete=fields.RESTRICT, description="下单用户"
    )
    address = fields.ForeignKeyField(
        "models.Address", on_delete=fields.RESTRICT, description="收货地址"
    )
    total_count = fields.IntField(default=1, description="商品总数")
    total_amount = fields.DecimalField(
        max_digits=10, decimal_places=2, description="商品总金额"
    )
    freight = fields.DecimalField(max_digits=10, decimal_places=2, description="运费")
    pay_method = fields.SmallIntField(default=1, description="支付方式")
    status = fields.SmallIntField(default=1, description="订单状态")

    class Meta:
        table = "m_order_info"

    def __str__(self):
        return self.order_id


class OrderGoods(models.Model):
    """订单商品"""

    SCORE_CHOICES = (
        (0, "0分"),
        (1, "20分"),
        (2, "40分"),
        (3, "60分"),
        (4, "80分"),
        (5, "100分"),
    )
    order = fields.ForeignKeyField(
        "models.OrderInfo",
        related_name="skus",
        on_delete=fields.CASCADE,
        description="订单",
    )
    sku = fields.ForeignKeyField(
        "models.SKU", on_delete=fields.RESTRICT, description="订单商品"
    )
    count = fields.IntField(default=1, description="数量")
    price = fields.DecimalField(max_digits=10, decimal_places=2, description="单价")
    comment = fields.TextField(default="", description="评价信息")
    score = fields.SmallIntField(default=5, description="满意度评分")
    is_anonymous = fields.BooleanField(default=False, description="是否匿名评价")
    is_commented = fields.BooleanField(default=False, description="是否评价了")

    class Meta:
        table = "m_order_goods"
