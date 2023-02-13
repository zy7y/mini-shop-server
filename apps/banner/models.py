from django.db import models

from apps.models import MallBaseModel


# imageField(upload_to = upload_path_handler)上传文件处理
def upload_path_handler(self, filename):
    """
    1. 上传到fastdfs 拿到文件地址
    2.保存文件地址到数据库
    """
    print(filename)


# Create your models here.
class Banner(MallBaseModel):
    img_url = models.ImageField(upload_to='banner', verbose_name="图片")
    to_link = models.URLField(verbose_name="跳转链接")
    name = models.CharField(max_length=20, verbose_name="名称")
    hidden = models.BooleanField(verbose_name="是否隐藏", default=False)
    sort = models.IntegerField(verbose_name="排序", default=999)

    class Meta:
        db_table = "dm_banner"
        verbose_name = "轮播图"
        verbose_name_plural = "轮播图管理"

    def __str__(self):
        return self.name
