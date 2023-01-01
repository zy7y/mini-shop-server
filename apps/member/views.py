import logging

from ninja import Router

from apps.member.schemas import MemberSchema
from apps.member.models import Member
from apps.schemas import R, Token
from utils.token import token_util

router = Router(tags=["会员管理"])

logger = logging.getLogger(__file__)


@router.post("", summary="创建用户", response=R[Token])
def create(request, data: MemberSchema):
    """
    小程序生成token
    :param request:
    :param data:
    :return:
    """
    # 1. 查询
    member = Member.objects.get(openid=data.openid)
    # 2. 创建
    if member is None:
        member = Member.objects.create(**data.dict())
    # 3. token生成
    token = token_util.build(member.openid)
    return R.ok(Token(token=token))



