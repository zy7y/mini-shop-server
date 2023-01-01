from ninja import ModelSchema

from apps.member.models import Member


class MemberSchema(ModelSchema):
    class Config:
        model = Member
        model_fields = '__all__'



