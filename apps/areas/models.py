from mall.model import fields, models


class Area(models.Model):
    name = fields.CharField(max_length=20, description="名称")
    parent: fields.ForeignKeyNullableRelation["Area"] = fields.ForeignKeyField(
        "models.Area",
        on_delete=fields.SET_NULL,
        related_name="subs",
        null=True,
        description="上级行政区划",
    )

    class Meta:
        table = "m_areas"
