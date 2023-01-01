from django.db import models

from apps.models import MallBaseModel


# Create your models here.

class Member(MallBaseModel):
    openid = models.CharField(max_length=128, verbose_name="openId", unique=True)
    avatar = models.CharField(max_length=129, verbose_name="头像")
    nickname = models.CharField(max_length=30, verbose_name="昵称")
    last_login = models.DateTimeField(auto_now=True, verbose_name="最后一次登录")

    class Meta:
        db_table = "dm_member"
        verbose_name = "会员"
        verbose_name_plural = "会员管理"

    def __str__(self):
        return self.nickname

    @classmethod
    def get(cls, openid: str):
        return cls.objects.get(openid=openid)