from mall.model import BaseModel, fields, models


class User(BaseModel):
    username = fields.CharField(max_length=150, description="账号", unique=True)
    password = fields.CharField(max_length=128, description="密码")
    email = fields.CharField(max_length=254, description="邮箱")
    is_staff = fields.BooleanField(default=False, description="后台管理员")

    class Meta:
        table = "fm_user"
        table_description = "用户"


class AddressManage(models.Manager):

    def get_default_address(self, user):
        return self.get_queryset().get(user=user, is_default=True)

    def get_all_address(self, user):
        return self.get_queryset().filter(user=user)


class Address(BaseModel):

    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    receiver = fields.CharField(max_length=20, description="收件人")
    addr = fields.CharField(max_length=256, description="收件地址")
    zip_code = fields.CharField(max_length=6, null=True, description="邮政编码")
    phone = fields.CharField(max_length=11, description="手机号")
    is_default = fields.BooleanField(default=False, description="是否默认")

    objects = AddressManage()

    class Meta:
        table = "fm_address"
        table_description = "收货地址"
