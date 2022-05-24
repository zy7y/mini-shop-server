from fastapi import FastAPI, applications
from tortoise import Tortoise

from apps.goods.search_es import to_es
from mall.conf import settings
from mall.exceptions import exception_handlers
from mall.urls import urlpatterns

# https://github.com/tiangolo/fastapi/issues/4924
def swagger_monkey_patch(*args, **kwargs):
    """
    Wrap the function which is generating the HTML for the /docs endpoint and
    overwrite the default values for the swagger js and css.
    """
    return get_swagger_ui_html(
        *args, **kwargs,
        swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.10.3/swagger-ui.css")


# Actual monkey patch
applications.get_swagger_ui_html = swagger_monkey_patch

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
    on_startup=[init, to_es],
    on_shutdown=[Tortoise.close_connections],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", reload=True)
