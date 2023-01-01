from django.contrib import admin

from apps.admin import MallAdmin
from apps.member.models import Member


# Register your models here.
@admin.register(Member)
class MemberAdmin(MallAdmin):
    list_display = ("nickname", 'avatar', 'last_login') + MallAdmin.list_display  # list

    # 禁用添加
    def has_add_permission(self, request):
        return False

    # 禁用删除
    def has_delete_permission(self, request, obj=None):
        return False

    # 禁用修改
    def has_change_permission(self, request, obj=None):
        return False



