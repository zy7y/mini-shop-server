from mall.model import BaseModel, fields


class ContentCategory(BaseModel):
    """广告分类"""

    name = fields.CharField(max_length=50, description="名称")
    key = fields.CharField(max_length=50, description="类别键名")

    class Meta:
        table = "m_content_category"


class Content(BaseModel):
    """广告内容"""

    category = fields.ForeignKeyField(
        "models.ContentCategory", on_delete=fields.CASCADE
    )
    title = fields.CharField(max_length=100, description="标题")
    url = fields.CharField(max_length=300, description="内容链接")
    image = fields.CharField(max_length=256, description="图片链接", null=True)
    text = fields.TextField(description="内容")
    sequence = fields.IntField(description="排序")
    status = fields.BooleanField(default=True, description="是否展示")

    class Meta:
        table = "m_content"
