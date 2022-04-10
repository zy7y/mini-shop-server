from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.routing import APIRoute

from .views import (
    Response,
    Token,
    auth,
    github_auth,
    github_auth_call,
    image_captcha,
    register,
    sms_captcha,
)

urlpatterns = [
    APIRoute(
        "/img_code/{uuid}",
        image_captcha,
        summary="图片验证码",
        response_class=StreamingResponse,
    ),
    APIRoute(
        "/sms_code/{mobile}", sms_captcha, summary="短信验证码", response_model=Response
    ),
    APIRoute(
        "/register",
        register,
        methods=["POST"],
        summary="用户注册",
        response_model=Response[Token],
    ),
    APIRoute(
        "/login", auth, methods=["POST"], summary="用户登录", response_model=Response[Token]
    ),
    APIRoute(
        "/github_auth", github_auth, summary="Github授权", response_class=RedirectResponse
    ),
    APIRoute(
        "/oauth/redirect",
        github_auth_call,
        summary="Github认证回调",
        include_in_schema=False,
        response_model=Response[Token],
    ),
]
