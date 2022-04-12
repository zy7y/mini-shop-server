from typing import List

from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.routing import APIRoute

from apps.user.bodys import AddressInfo, UserInfo
from apps.user.views import (address_list, auth, create_address,
                             default_address, del_address, github_auth,
                             github_auth_call, image_captcha, register,
                             sms_captcha, update_address, update_email,
                             update_password, update_title_address, user_info,
                             verify_email)
from mall.bodys import Response, Token

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
        "/emails",
        update_email,
        methods=["put"],
        summary="修改邮箱",
        response_model=Response,
        tags=["用户中心"],
    ),
    APIRoute(
        "/emails/verification",
        verify_email,
        methods=["get"],
        summary="激活邮箱",
        response_model=Response,
        tags=["用户中心"],
    ),
    APIRoute(
        "/addresses/create",
        create_address,
        methods=["post"],
        summary="新增地址",
        response_model=Response[AddressInfo],
        tags=["用户中心"],
    ),
    APIRoute(
        "/addresses",
        address_list,
        summary="地址列表",
        response_model=Response[List[AddressInfo]],
        tags=["用户中心"],
    ),
    APIRoute(
        "/addresses/{pk}",
        update_address,
        methods=["put"],
        summary="修改地址",
        response_model=Response[AddressInfo],
        tags=["用户中心"],
    ),
    APIRoute(
        "/addresses/{pk}",
        del_address,
        methods=["delete"],
        summary="删除地址",
        response_model=Response,
        tags=["用户中心"],
    ),
    APIRoute(
        "/addresses/{pk}/default",
        default_address,
        methods=["put"],
        summary="设置默认地址",
        response_model=Response,
        tags=["用户中心"],
    ),
    APIRoute(
        "/addresses/{pk}/title",
        update_title_address,
        methods=["put"],
        summary="设置地址标题",
        response_model=Response,
        tags=["用户中心"],
    ),
    APIRoute(
        "/password",
        update_password,
        methods=["put"],
        summary="修改密码",
        response_model=Response,
        tags=["用户中心"],
    ),
]
