from fastapi import FastAPI
from tortoise import Tortoise

from mall.conf import settings
from mall.exceptions import exception_handlers
from mall.urls import urlpatterns


async def init():
    await Tortoise.init(
        db_url=settings.MYSQL_DATABASE_URL, modules={"models": settings.APP_MODELS}
    )


app = FastAPI(
    title="美多商城",
    description="""
- 使用FastAPI构建的美多商城项目
- 源项目使用Django， 构建参考视频https://www.bilibili.com/video/BV1ya411A7C8
""",
    exception_handlers=exception_handlers,
    routes=urlpatterns,
    on_startup=[init],
    on_shutdown=[Tortoise.close_connections],
)
