from fresh_mall.model import BaseModel, fields


class GoodsType(BaseModel):
    name = fields.CharField(max_length=20, description="种类名称")
    logo = fields.CharField(max_length=20, description="标识")
    image = fields.CharField(max_length=254, description="商品类型图片url")

    class Meta:
        table = "fm_goods_type"
        table_description = "商品种类"


class GoodsSKU(BaseModel):
    status_choices = (
        (0, "下线"),
        (1, "上线"),
    )

    type = fields.ForeignKeyField("models.GoodsType", description="商品种类", on_delete=fields.CASCADE)
    goods = fields.ForeignKeyField("models.Goods", description="商品SPU", on_delete=fields.CASCADE)
    name = fields.CharField(max_length=20, description="商品名称")
    desc = fields.CharField(max_length=256, description="商品简介")
    price = fields.DecimalField(max_digits=10, decimal_places=2, description="商品价格")
    unite = fields.CharField(max_length=20, verbose_name="商品单位")
    image = fields.CharField(max_length=256, description="商品图片")
    stock = fields.IntField(default=1, description="商品库存")
    sales = fields.IntField(default=0, description="商品销量")
    status = fields.SmallIntField(
        default=1, description="商品状态" + str(status_choices)
    )

    class Meta:
        table = "fm_goods_sku"
        table_description = "商品表"


class Goods(BaseModel):
    name = fields.CharField(max_length=20, description="商品SPU名称")
    detail = fields.TextField(description="商品详情")

    class Meta:
        table = "fm_goods"
        table_description = "商品SPU"


class GoodsImage(BaseModel):
    sku = fields.ForeignKeyField("models.GoodsSKU", on_delete=fields.RESTRICT)
    image = fields.CharField(max_length=256, description="图片")

    class Meta:
        table = "fm_goods_image"
        table_description = "商品图片"


class IndexGoodsBanner(BaseModel):
    sku = fields.ForeignKeyField("models.GoodsSKU", on_delete=fields.RESTRICT)
    image = fields.CharField(max_length=254, description="图片")
    index = fields.SmallIntField(default=0, description="展示顺序")

    class Meta:
        table = "fm_index_banner"
        table_description = "首页轮播商品"


class IndexTypeGoodsBanner(BaseModel):
    """首页分类商品展示模型类"""

    DISPLAY_TYPE_CHOICES = ((0, "标题"), (1, "图片"))

    type = fields.ForeignKeyField(
        "models.GoodsType", description="商品类型", on_delete=fields.RESTRICT
    )
    sku = fields.ForeignKeyField(
        "models.GoodsSKU", description="商品SKU", on_delete=fields.RESTRICT
    )
    display_type = fields.SmallIntField(
        default=1, description="展示类型" + str(DISPLAY_TYPE_CHOICES)
    )
    index = fields.SmallIntField(default=0, description="展示顺序")

    class Meta:
        table = "fm_index_type_goods"
        table_description = "主页分类展示商品"


class IndexPromotionBanner(BaseModel):
    """首页促销活动模型类"""

    name = fields.CharField(max_length=20, description="活动名称")
    url = fields.CharField(max_length=254, description="活动链接")
    image = fields.CharField(max_length=254, description="活动图片")
    index = fields.SmallIntField(default=0, description="展示顺序")

    class Meta:
        table = "fm_index_promotion"
        table_description = "主页促销活动"
