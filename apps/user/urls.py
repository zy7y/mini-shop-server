from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.routing import APIRoute

from mall.bodys import Response, Token

from .bodys import UserInfo
from .views import (
    auth,
    github_auth,
    github_auth_call,
    image_captcha,
    register,
    sms_captcha,
    update_email,
    user_info,
)

urlpatterns = [
    APIRoute(
        "/img_code/{uuid}",
        image_captcha,
        summary="图片验证码",
        response_class=StreamingResponse,
        tags=["公共服务"],
    ),
    APIRoute(
        "/sms_code/{mobile}",
        sms_captcha,
        summary="短信验证码",
        response_model=Response,
        tags=["公共服务"],
    ),
    APIRoute(
        "/register",
        register,
        methods=["POST"],
        summary="用户注册",
        response_model=Response[Token],
        tags=["用户认证"],
    ),
    APIRoute(
        "/login",
        auth,
        methods=["POST"],
        summary="用户登录",
        response_model=Response[Token],
        tags=["用户认证"],
    ),
    APIRoute(
        "/github_auth",
        github_auth,
        summary="Github授权",
        response_class=RedirectResponse,
        tags=["用户认证"],
    ),
    APIRoute(
        "/oauth/redirect",
        github_auth_call,
        summary="Github认证回调",
        include_in_schema=False,
        response_model=Response[Token],
        tags=["用户认证"],
    ),
    APIRoute(
        "/info",
        user_info,
        summary="获取用户信息",
        response_model=Response[UserInfo],
        tags=["用户中心"],
    ),
    APIRoute(
        "/emails", update_email, summary="修改邮箱", response_model=Response, tags=["用户中心"]
    ),
]
