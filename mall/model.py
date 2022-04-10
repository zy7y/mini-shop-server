from tortoise import fields, models


class BaseModel(models.Model):
    create_time = fields.DatetimeField(auto_now_add=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")
    is_delete = fields.BooleanField(default=False, description="删除标记")

    class Meta:
        abstract = True
