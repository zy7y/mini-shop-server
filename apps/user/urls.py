from fastapi.routing import APIRoute
from fastapi.responses import StreamingResponse

from .views import register, Response, Token, sms_captcha, image_captcha

urlpatterns = [
    APIRoute("/img_code/{uuid}", image_captcha, summary="图片验证码", response_class=StreamingResponse),
    APIRoute("/sms_code/{mobile}", sms_captcha, summary="短信验证码", response_model=Response),
    APIRoute("/register", register, methods=["POST"], response_model=Response[Token])
]