from django.contrib import admin

from apps.address.models import Address
from apps.admin import MallAdmin


# Register your models here.
@admin.register(Address)
class AddressAdmin(MallAdmin):
    list_display = ("member", 'detail', 'receiver', 'phone') + MallAdmin.list_display  # list