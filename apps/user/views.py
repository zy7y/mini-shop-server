import requests
from fastapi import Depends, Path
from fastapi.encoders import jsonable_encoder
from simpel_captcha import captcha, img_captcha
from starlette.responses import StreamingResponse
from tortoise.expressions import Q
from tortoise.fields.relational import _NoneAwaitable

from apps.areas.models import Area
from apps.user.bodys import (AddressCreate, AddressTitle, AddressUpdate,
                             EmailBody, PasswordUpdate, Register, UserAuth,
                             UserInfo)
from apps.user.models import Address, OAuthGithub, User
from celery_tasks.tasks import async_send_email, sms_code
from mall.bodys import Response
from mall.conf import settings
from mall.security import (check_token, check_token_http, create_access_token,
                           get_password_hash, verify_password)
from mall.tools import img_code_redis, sms_code_redis

mobile_regx = r"^1(3\d|4[5-9]|5[0-35-9]|6[567]|7[0-8]|8\d|9[0-35-9])\d{8}$"


async def image_captcha(uuid: str):
    """获取图片验证码"""
    img, text = img_captcha(byte_stream=True)
    # 缓存redis 验证码过期时间100s
    await img_code_redis.setex(uuid, 100, text)
    return StreamingResponse(img, media_type="image/jpeg")


async def sms_captcha(
    mobile: str = Path(..., regex=mobile_regx), *, img_code: str, uuid: str
):
    """发短信验证码"""
    redis_value = await img_code_redis.get(uuid)
    # 删除图片验证码
    await img_code_redis.delete(uuid)

    if redis_value != img_code:
        return Response(code=400, errmsg="图片验证码错误")

    # 是否60秒内已发送
    if await sms_code_redis.get(f"flag_{mobile}"):
        return Response(code=400, errmsg="频繁发送短信验证码")

    text = captcha(6)

    # 批量操作
    async with sms_code_redis.pipeline(transaction=True) as pipe:
        save_time = 300  # s
        # 保存手机号和验证码
        await (
            pipe.setex(mobile, save_time, text)
            # 标记发送 60s 失效
            .setex(f"flag_{mobile}", 60, 1).execute()
        )

    sms_code.delay(mobile, text, save_time / 60)
    return Response(data={"code": text})


async def register(user: Register):
    # 验证同意协议
    if not user.allow:
        return Response(code=400, errmsg="请同意协议")
    # 验证密码一致
    if user.password != user.sure_password:
        return Response(code=400, errmsg="两次密码不一致")

    # 验证短信验证码正确
    if user.sms_code != await sms_code_redis.get(user.mobile):
        return Response(code=400, errmsg="短信验证码错误")

    # 保证一个验证码只能用一次
    await sms_code_redis.delete(user.mobile)

    # 验证账号是否存在
    if (
        await User.get_or_none(
            Q(username=user.username) | Q(mobile=user.mobile) | Q(email=user.email)
        )
        is not None
    ):
        return Response(code=400, errmsg="用户已注册")

    user.password = get_password_hash(user.password)
    delattr(user, "allow")
    delattr(user, "sure_password")
    delattr(user, "sms_code")
    await User.create(**user.dict())
    return Response(data={"access_token": create_access_token(username=user.username)})


async def auth(user: UserAuth):
    """多账号登录"""
    user_obj = await User.get_or_none(
        Q(username=user.username) | Q(mobile=user.username)
    )
    if user_obj is not None:
        if verify_password(user.password, user_obj.password):
            return Response(
                data={"access_token": create_access_token(username=user.username)}
            )
    return Response(code=400, errmsg="账号或密码错误")


# http://127.0.0.1:8000/oauth/redirect github oauth 回调地址
def github_auth():
    """github 授权"""
    return settings.GITHUB_OAUTH_PAGE


async def github_auth_call(code: str):
    """github 授权的回调，实际业务操作"""
    try:
        github_token_url = "https://github.com/login/oauth/access_token"
        data = {
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "code": code,
        }
        result = requests.post(
            url=github_token_url, json=data, headers={"Accept": "application/json"}
        )
        github_token = result.json().get("access_token")
        # 获取当前认证的github 用户信息
        github_info = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"token {github_token}"},
        ).json()
    except Exception as e:
        return Response(code=400, errmsg=str(e))

    user_obj = await OAuthGithub.get_or_none(openid=github_info.get("id"))
    # 用户存在直接登录
    if user_obj is not None:
        user = await user_obj.user
    else:
        # 用户不存在, 则注册密码默认 m123456
        user = await User.create(
            username=github_info.get("login"),
            password=get_password_hash("m123456"),
            email="",
            mobile="",
        )
        await OAuthGithub.create(openid=github_info.get("id"), user=user)

    return Response(data={"access_token": create_access_token(username=user.username)})


async def user_info(user: User = Depends(check_token_http)):
    """获取当前用户信息"""
    data = UserInfo(
        id=user.pk,
        username=user.username,
        mobile=user.mobile,
        email=user.email,
        is_active=user.is_active,
    )
    return Response(data=data)


async def update_email(
    email_body: EmailBody, *, user: User = Depends(check_token_http)
):
    """修改邮箱"""
    if user.email == email_body.email:
        return Response(code=400, errmsg="修改无效")

    result = await user.filter(Q(id=user.pk), Q(is_delete=False)).update(
        email=email_body.email
    )
    if result:
        href = f"http://127.0.0.1:8000/emails/verification?token={create_access_token(user.username)}"
        async_send_email.delay(email_body.email, href)
        return Response()
    return Response(code=400, errmsg="账号已删除")


async def verify_email(token: str):
    """激活邮箱"""
    if user := await check_token(token):
        if user.is_active:
            return Response(code=400, errmsg="无需重新激活")
        result = await user.filter(
            Q(id=user.pk), Q(is_delete=False), ~Q(email="")
        ).update(is_active=True)
        if result:
            return Response()
    return Response(code=400, errmsg="账号有误,请联系管理员")


async def create_address(
    address: AddressCreate, user: User = Depends(check_token_http)
):
    """新增地址"""
    if await Address.filter(user=user).count() > 20:
        return Response(code=400, errmsg="超过地址数量上限")

    # 2. 查 省
    province = await Area.get_or_none(pk=address.province_id)
    if province is None:
        return Response(code=400, errmsg="省份不存在")
    # 3. 查 市
    city = await Area.get_or_none(Q(pk=address.city_id), Q(parent=province))
    if city is None:
        return Response(code=400, errmsg="市区不存在")

    # 4. 查区
    district = await Area.get_or_none(Q(pk=address.district_id))
    if district is None:
        return Response(code=400, errmsg="区县不存在")

    del address.province_id
    del address.city_id
    del address.district_id

    address_obj = await Address.create(
        **address.dict(),
        title=address.receiver,
        user=user,
        province=province,
        city=city,
        district=district,
    )
    # 默认地址
    if isinstance(user.default_address, _NoneAwaitable):
        await user.filter(default_address=None).update(default_address=address_obj)
    return Response(
        data={
            **jsonable_encoder(address_obj),
            "province": address_obj.province.name,
            "city": address_obj.city.name,
            "district": address_obj.district.name,
        }
    )


async def address_list(user: User = Depends(check_token_http)):
    """地址列表"""
    address_arr = await Address.filter(user_id=user.pk, is_delete=False).all()
    data = []
    for address in address_arr:
        province = await Area.get(pk=address.province_id)
        city = await Area.get(pk=address.city_id)
        district = await Area.get(pk=address.district_id)
        item = {
            **jsonable_encoder(address),
            "province": province.name,
            "city": city.name,
            "district": district.name,
        }
        if user.default_address_id == address.pk:
            data.insert(0, item)
        else:
            data.append(item)
    return Response(data=data)


async def update_address(
    pk: int, address: AddressUpdate, user: User = Depends(check_token_http)
):
    """修改地址"""
    if (obj := await Address.get_or_none(pk=pk)) is not None:
        # 2. 查 省
        province = await Area.get_or_none(pk=address.province_id)
        if province is None:
            return Response(code=400, errmsg="省份不存在")
        # 3. 查 市
        city = await Area.get_or_none(Q(pk=address.city_id), Q(parent=province))
        if city is None:
            return Response(code=400, errmsg="市区不存在")

        # 4. 查区
        district = await Area.get_or_none(Q(pk=address.district_id))
        if district is None:
            return Response(code=400, errmsg="区县不存在")

        # 会返回更新数量
        await obj.filter(id=pk).update(**address.dict())

        return Response(
            data={
                **jsonable_encoder(address),
                "province": province.name,
                "city": city.name,
                "district": district.name,
            }
        )
    return Response(code=400, errmsg="更新地址失败")


async def del_address(pk: int, user: User = Depends(check_token_http)):
    """删除地址"""
    obj = await Address.get_or_none(pk=pk)
    if obj is not None:
        obj.is_delete = True
        await obj.save()
        return Response()
    return Response(code=400, errmsg="地址删除失败")


async def default_address(pk: int, user: User = Depends(check_token_http)):
    """设置默认地址"""
    address = await Address.get_or_none(pk=pk)
    if address is not None:
        user.default_address = address
        await user.save()
        return Response()
    return Response(code=400, errmsg="设置默认地址失败")


async def update_title_address(
    pk: int, title: AddressTitle, user: User = Depends(check_token_http)
):
    """设置地址标题"""
    address = await Address.get_or_none(pk=pk)
    if address is not None:
        address.title = title.title
        await address.save()
        return Response()
    return Response(code=400, errmsg="设置地址标题失败")


async def update_password(
    password_body: PasswordUpdate, user: User = Depends(check_token_http)
):
    if password_body.old_password == password_body.new_password:
        return Response(code=400, errmsg="新老密码不能一致")

    if password_body.new_password != password_body.sure_password:
        return Response(code=400, errmsg="两次密码不一致")

    if not verify_password(password_body.old_password, user.password):
        return Response(code=400, errmsg="原始密码错误")

    user.password = get_password_hash(password_body.new_password)
    await user.save()
    return Response()
