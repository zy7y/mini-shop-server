from .models import User
from .bodys import Register
from mall.bodys import Response
from mall.security import get_password_hash

from mall.tools import RedisManager

# 获取一个redis 库 序号为0
active_flag = RedisManager.get(0)
# 300s
flag_time = 300


async def register(user: Register):
    if not user.allow:
        return Response(code=400, msg="请同意协议")

    user.password = get_password_hash(user.password)
    delattr(user, "allow")

    # 激活邮件 缓存redis
    await active_flag.setex(user.username, flag_time, get_password_hash(user.username))
    # 异步发送邮件



    # user_obj = await User.create(**user.dict())


    return Response(code=200,  msg="ok")