from fastapi import FastAPI
from fresh_mall.exceptions import exception_handlers
from fresh_mall.urls import urlpatterns
from fresh_mall.conf import settings

from tortoise import Tortoise


async def init():
    await Tortoise.init(
        db_url=settings.MYSQL_DATABASE_URL,
        modules={'models': settings.APP_MODELS}
    )

app = FastAPI(
    title="天天生鲜 RestFUL",
    description="""
- 使用FastAPI构建的天天生鲜商城项目
- 源项目使用Django， 构建参考视频https://www.bilibili.com/video/BV1vt41147K8
""",
    exception_handlers=exception_handlers,
    routes=urlpatterns,
    on_startup=[init],
    on_shutdown=[Tortoise.close_connections]
)