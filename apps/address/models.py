from django.db import models

from apps.member.models import Member
from apps.models import MallBaseModel


# Create your models here.


class Address(MallBaseModel):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="addresses")
    province = models.CharField(max_length=20, verbose_name="省")
    city = models.CharField(max_length=20, verbose_name="市")
    district = models.CharField(max_length=20, verbose_name="区")
    detail = models.CharField(max_length=128, verbose_name="详细地址")
    phone = models.CharField(max_length=11, verbose_name="联系电话")
    receiver = models.CharField(max_length=10, verbose_name="联系人")
    is_default = models.BooleanField(default=False, verbose_name="是否默认")

    class Meta:
        db_table = "dm_address"
        verbose_name = "地址"
        verbose_name_plural = "地址管理"

    def __str__(self):
        return self.member.nickname
