from mall.model import BaseModel, fields


class GoodsCategory(BaseModel):
    """商品分类"""

    name = fields.CharField(max_length=10, description="名称")
    parent = fields.ForeignKeyField(
        "models.GoodsCategory", related_name="subs", null=True, on_delete=fields.CASCADE
    )

    class Meta:
        table = "m_goods_category"


class GoodsChannelGroup(BaseModel):
    """商品频道分组"""

    name = fields.CharField(max_length=20, description="频道组名")

    class Meta:
        table = "m_channel_group"


class GoodsChannel(BaseModel):
    """商品频道"""

    group = fields.ForeignKeyField("models.GoodsChannelGroup", on_delete=fields.CASCADE)
    category = fields.ForeignKeyField("models.GoodsCategory", on_delete=fields.CASCADE)
    url = fields.CharField(max_length=50, description="频道页面链接")
    sequence = fields.IntField(description="排序")

    class Meta:
        table = "m_goods_channel"


class Brand(BaseModel):
    """品牌"""

    name = fields.CharField(max_length=20, description="名称")
    logo = fields.CharField(max_length=254, description="logo 图片链接")
    first_letter = fields.CharField(max_length=1, description="品牌首字母")

    class Meta:
        table = "m_brand"


class SPU(BaseModel):
    """商品SPU"""

    name = fields.CharField(max_length=50, description="名称")
    brand = fields.ForeignKeyField("models.Brand", on_delete=fields.RESTRICT)
    category1 = fields.ForeignKeyField(
        "models.GoodsCategory", on_delete=fields.RESTRICT, related_name="cat1_spu"
    )
    category2 = fields.ForeignKeyField(
        "models.GoodsCategory", on_delete=fields.RESTRICT, related_name="cat2_spu"
    )
    category3 = fields.ForeignKeyField(
        "models.GoodsCategory", on_delete=fields.RESTRICT, related_name="cat3_spu"
    )
    sales = fields.IntField(default=0, description="销量")
    comments = fields.IntField(default=0, description="评价数")
    desc_detail = fields.TextField(default="", description="详细介绍")
    desc_pack = fields.TextField(default="", description="包装信息")
    desc_service = fields.TextField(default="", description="售后服务")

    class Meta:
        table = "m_spu"


class SKU(BaseModel):
    name = fields.CharField(max_length=50, description="名称")
    caption = fields.CharField(max_length=100, description="副标题")
    spu = fields.ForeignKeyField(
        "models.SPU", on_delete=fields.CASCADE, description="商品"
    )
    category = fields.ForeignKeyField(
        "models.GoodsCategory", on_delete=fields.RESTRICT, description="从属类别"
    )
    price = fields.DecimalField(max_digits=10, decimal_places=2, description="单价")
    cost_price = fields.DecimalField(max_digits=10, decimal_places=2, description="进价")
    market_price = fields.DecimalField(
        max_digits=10, decimal_places=2, description="市场价"
    )
    stock = fields.IntField(default=0, description="库存")
    sales = fields.IntField(default=0, description="销量")
    comments = fields.IntField(default=0, description="评价数")
    is_launched = fields.BooleanField(default=True, description="是否上架销售")
    default_image = fields.CharField(
        max_length=200, default="", null=True, description="默认图片 url"
    )

    class Meta:
        table = "m_sku"


class SKUImage(BaseModel):
    """SKU图片"""

    sku = fields.ForeignKeyField(
        "models.SKU", on_delete=fields.CASCADE, description="sku"
    )
    image = fields.CharField(max_length=256, description="图片 url")

    class Meta:
        table = "m_sku_image"
        table_description = "SKU图片"


class SPUSpecification(BaseModel):
    """商品SPU规格"""

    spu = fields.ForeignKeyField(
        "models.SPU",
        on_delete=fields.CASCADE,
        related_name="specs",
        description="商品SPU",
    )
    name = fields.CharField(max_length=20, description="规格名称")

    class Meta:
        table = "m_spu_specification"
        table_description = "商品SPU规格"


class SpecificationOption(BaseModel):
    """规格选项"""

    spec = fields.ForeignKeyField(
        "models.SPUSpecification",
        related_name="options",
        on_delete=fields.CASCADE,
        description="规格",
    )
    value = fields.CharField(max_length=20, description="选项值")

    class Meta:
        table = "m_specification_option"
        table_description = "规格选项"


class SKUSpecification(BaseModel):
    """SKU具体规格"""

    sku = fields.ForeignKeyField(
        "models.SKU", related_name="specs", on_delete=fields.CASCADE, description="sku"
    )
    spec = fields.ForeignKeyField(
        "models.SPUSpecification", on_delete=fields.RESTRICT, description="规格名称"
    )
    option = fields.ForeignKeyField(
        "models.SpecificationOption", on_delete=fields.RESTRICT, description="规格值"
    )

    class Meta:
        table = "m_sku_specification"
        table_description = "SKU规格"


class GoodsVisitCount(BaseModel):
    """统计分类商品数量"""

    category = fields.ForeignKeyField("models.GoodsCategory", on_delete=fields.CASCADE)
    count = fields.IntField(description="访问量", default=0)
    date = fields.DateField(auto_now_add=True, description="统计日期")

    class Meta:
        table = "m_goods_visit"
