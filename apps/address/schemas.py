from ninja import ModelSchema

from apps.address.models import Address


class AddressSchema(ModelSchema):
    class Config:
        model = Address
        model_exclude = ['member']

