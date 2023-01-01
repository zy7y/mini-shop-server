from django.db import models


class MallBaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", null=True)
    updated = models.DateTimeField(auto_now=True, verbose_name="更新时间", null=True)

    class Meta:
        abstract = True
