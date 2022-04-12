from ronglian_sms_sdk import SmsSDK
from yagmail import SMTP

from celery_tasks.main import celery_app
from mall.conf import settings


@celery_app.task
def sms_code(mobile: str, captcha: str, minute: int, tid: str = "1"):
    """celery 装饰 异步
    发送短信验证码
    :param mobile: 发送手机号，多个手机号使用 , 分割
    :param captcha: 验证码
    :param minute: 失效时间(分钟)
    :param tid: 模板 免费模板 默认为 '1'
    """
    sdk = SmsSDK(settings.ACCOUNT_SID, settings.ACCOUNT_TOKEN, settings.APPID)
    return sdk.sendMessage(tid, mobile, (captcha, str(minute)))


@celery_app.task
def async_send_email(to: str, href: str):
    """异步 发送邮件
    :param to: 收件人
    :param href: 激活链接
    """
    # https://blog.csdn.net/weixin_38428827/article/details/104223207
    with SMTP(
        user=settings.EMAIL_USER,
        password=settings.EMAIL_SECRET,
        host=settings.EMAIL_SMTP_HOST,
    ) as y:

        y.send(
            to,
            "美多商城邮箱验证",
            contents=f"""
        <p>尊敬的用户您好！</p>
        <p>感谢您使用美多商城。</p>
        <p>您的邮箱为：{to} 。请点击此链接激活您的邮箱：</p>
        '<p><a href="{href}">{href}<a></p>'
        """,
        )
