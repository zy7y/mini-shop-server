from ninja.security import HttpBearer

from apps.member.models import Member
from utils.token import token_util


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        openid = token_util.parse(token)
        request.user = Member.get(openid=openid)
        return openid
