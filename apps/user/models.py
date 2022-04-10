from mall.model import BaseModel, fields


class User(BaseModel):
    username = fields.CharField(max_length=150, description="账号", unique=True)
    password = fields.CharField(max_length=128, description="密码")
    email = fields.CharField(max_length=254, description="邮箱", unique=True)
    mobile = fields.CharField(max_length=11, description="手机号", unique=True)
    is_staff = fields.BooleanField(default=False, description="是否管理员")
    is_active = fields.BooleanField(default=False, description="是否激活")

    class Meta:
        table = "m_user"


class OAuthGithub(BaseModel):
    user = fields.ForeignKeyField("models.User", on_delete=fields.CASCADE)
    openid = fields.CharField(max_length=64, description="用户OpenID", index=True)

    class Meta:
        table = "m_oauth_github"
