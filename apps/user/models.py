from mall.model import BaseModel, fields


class User(BaseModel):
    username = fields.CharField(max_length=150, description="账号", unique=True)
    password = fields.CharField(max_length=128, description="密码")
    email = fields.CharField(max_length=254, description="邮箱", unique=True)
    mobile = fields.CharField(max_length=11, description="手机号", unique=True)
    is_staff = fields.BooleanField(default=False, description="是否管理员")
    is_active = fields.BooleanField(default=False, description="是否激活")
    default_address = fields.ForeignKeyField(
        "models.Address", on_delete=fields.SET_NULL, null=True, description="默认收获地址"
    )

    class Meta:
        table = "m_user"


class OAuthGithub(BaseModel):
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    openid = fields.CharField(max_length=64, description="用户OpenID", index=True)

    class Meta:
        table = "m_oauth_github"


class Address(BaseModel):
    user = fields.ForeignKeyField(
        "models.User", on_delete=fields.CASCADE, related_name="addresses"
    )
    title = fields.CharField(max_length=20, description="地址名称")
    receiver = fields.CharField(max_length=20, description="收货人")
    # 最终指向的是apps.areas.models.Area
    province = fields.ForeignKeyField(
        "models.Area",
        on_delete=fields.RESTRICT,
        related_name="province_addresses",
        description="省",
    )
    city = fields.ForeignKeyField(
        "models.Area",
        on_delete=fields.RESTRICT,
        description="市",
        related_name="city_addresses",
    )
    district = fields.ForeignKeyField(
        "models.Area",
        on_delete=fields.RESTRICT,
        description="区",
        related_name="district_addresses",
    )
    place = fields.CharField(max_length=50, description="地址")
    mobile = fields.CharField(max_length=11, description="手机号")
    tel = fields.CharField(max_length=20, description="固定电话", null=True, default="")
    email = fields.CharField(max_length=30, null=True, default="", description="电子邮箱")

    class Meta:
        table = "m_address"
        table_description = "收获地址"
        ordering = ("-update_time",)
