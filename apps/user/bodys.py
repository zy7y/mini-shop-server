# 入参模型定义

from pydantic import EmailStr, Field
from mall.bodys import BaseBody


class Register(BaseBody):
    username: str = Field(..., description="账号", min_length=5)
    password: str = Field(..., description="密码", min_length=6)
    email: EmailStr = Field(..., description="邮箱")
    allow: bool = Field(default=False, description="是否同意用户协议")

