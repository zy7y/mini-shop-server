from ninja import ModelSchema

from apps.banner.models import Banner


class BannerSchema(ModelSchema):
    class Config:
        model = Banner
        model_fields = '__all__'
