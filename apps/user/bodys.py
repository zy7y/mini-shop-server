# 入参模型定义
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

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


class UserInfo(BaseModel):
    id: int
    username: str
    mobile: str
    email: str
    is_active: str = Field(..., description="邮箱是否激活")


class EmailBody(BaseModel):
    email: EmailStr = Field(..., description="邮箱")


class AddressBase(BaseBody):
    receiver: str = Field(..., description="收货人")
    place: str = Field(..., description="收货地址")
    mobile: str = Field(..., regex=r"1[3-9]\d{9}$", description="手机号")
    tel: Optional[str] = Field(
        None,
        regex=r"^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$",
        description="固定电话",
    )
    email: Optional[EmailStr] = Field(None, description="邮箱")


class AddressCreate(AddressBase):
    province_id: int = Field(..., description="省份ID")
    city_id: int = Field(..., description="城市ID")
    district_id: int = Field(..., description="区县ID")


class AddressTitle(BaseBody):
    title: str


class AddressInfo(AddressBase, AddressTitle):
    """展示地址信息"""

    id: int
    province: str = Field(..., description="省")
    city: str = Field(..., description="市")
    district: str = Field(..., description="区")


class AddressUpdate(AddressCreate):
    pass


class PasswordUpdate(BaseBody):
    old_password: str = Field(..., description="老密码", min_length=6)
    new_password: str = Field(..., description="新密码", min_length=6)
    sure_password: str = Field(..., description="确认密码", min_length=6)
