# 入参模型定义

from pydantic import EmailStr, Field
from mall.bodys import BaseBody


class UserBodyBase(BaseBody):
    username: str = Field(..., description="账号", min_length=5)
    password: str = Field(..., description="密码", min_length=6)


class Register(UserBodyBase):
    sure_password: str = Field(..., description="确认密码", min_length=6)
    email: EmailStr = Field(..., description="邮箱")
    mobile: str = Field(..., regex=r"1[3-9]\d{9}$", description="手机号")
    allow: bool = Field(default=False, description="是否同意用户协议")
    sms_code: str = Field(..., description="短信验证码", min_length=6, max_length=6)


class UserAuth(UserBodyBase):
    remembered: bool = Field(True, description="是否记住")
