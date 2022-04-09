from typing import Dict

from fdfs_client.client import Fdfs_client
from aioredis import from_url, Redis
from yagmail import SMTP
from ronglian_sms_sdk import SmsSDK

from .conf import settings

# FastDFS 客户端
FastDFSManager = Fdfs_client(settings.TRACKER_ADDRESS)

# Redis 客户端
RedisManager: Dict[int, Redis] = {
    db: from_url(settings.REDIS_URL, db=db, max_connections=10, encoding="utf-8",
                 decode_responses=True)
    for db in range(16)
}


def send_email(to: str, href: str):
    """发送邮件
    :param to: 收件人
    :param href: 激活链接
    """
    # https://blog.csdn.net/weixin_38428827/article/details/104223207
    with SMTP(user=settings.EMAIL_USER,
              password=settings.EMAIL_SECRET, host=settings.EMAIL_SMTP_HOST) as y:
        y.send(to, '邮箱验证', contents=f"""
        <p> 邮箱: {to}</p>
        <p><a href={href}>👇me</a></p>
        """)


def send_message(mobile: str, captcha: str, minute: int, tid: str = '1'):
    """
    发送短信验证码
    :param mobile: 发送手机号，多个手机号使用 , 分割
    :param captcha: 验证码
    :param minute: 失效时间(分钟)
    :param tid: 模板 免费模板 默认为 '1'
    """
    sdk = SmsSDK(settings.ACCOUNT_SID, settings.ACCOUNT_TOKEN, settings.APPID)
    return sdk.sendMessage(tid, mobile, (captcha, str(minute)))