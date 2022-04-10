from fastapi import Path
from simpel_captcha import img_captcha, captcha
from starlette.responses import StreamingResponse
from tortoise.expressions import Q

from .models import User
from .bodys import Register, UserAuth
from mall.bodys import Response, Token
from mall.security import get_password_hash, create_access_token, verify_password
from mall.tools import img_code_redis, sms_code_redis
from celery_tasks.tasks import sms_code

mobile_regx = r'^1(3\d|4[5-9]|5[0-35-9]|6[567]|7[0-8]|8\d|9[0-35-9])\d{8}$'


async def image_captcha(uuid: str):
    """获取图片验证码"""
    img, text = img_captcha(byte_stream=True)
    # 缓存redis 验证码过期时间100s
    await img_code_redis.setex(uuid, 100, text)
    return StreamingResponse(img, media_type='image/jpeg')


async def sms_captcha(mobile: str = Path(..., regex=mobile_regx), *, img_code: str, uuid: str):
    """发短信验证码"""
    redis_value = await img_code_redis.get(uuid)
    # 删除图片验证码
    await img_code_redis.delete(uuid)

    if redis_value != img_code:
        return Response(code=400, errmsg='图片验证码错误')

    # 是否60秒内已发送
    if await sms_code_redis.get(f"flag_{mobile}"):
        return Response(code=400, errmsg='频繁发送短信验证码')

    text = captcha(6)

    # 批量操作
    async with sms_code_redis.pipeline(transaction=True) as pipe:
        save_time = 300  # s
        # 保存手机号和验证码
        await (pipe.setex(mobile, save_time, text)
               # 标记发送 60s 失效
               .setex(f"flag_{mobile}", 60, 1)
               .execute()
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
    if await User.get_or_none(username=user.username) is not None:
        return Response(code=400, errmsg="用户已注册")

    user.password = get_password_hash(user.password)
    delattr(user, "allow")
    delattr(user, "sure_password")
    delattr(user, "sms_code")
    await User.create(**user.dict())
    data = Token(access_token=create_access_token(username=user.username))
    return Response(data=data)


async def auth(user: UserAuth):
    """多账号登录"""

    user_obj = await User.get_or_none(Q(username=user.username) | Q(mobile=user.username))
    if user_obj is not None:
        if verify_password(user.password, user_obj.password):
            data = Token(access_token=create_access_token(username=user.username))
            return Response(data=data)
    return Response(code=400, errmsg='账号或密码错误')

