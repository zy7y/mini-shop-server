from django.contrib import admin

from apps.admin import MallAdmin
from apps.banner.models import Banner


# Register your models here.
@admin.register(Banner)
class BannerAdmin(MallAdmin):
    list_display = (
        "name",
        'img_url',
        'to_link',
        'sort',
        'hidden',
    ) + MallAdmin.list_display  # list
