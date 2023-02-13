from django.contrib import admin


class MallAdmin(admin.ModelAdmin):
    """
    基础模块，由其他系统模块继承 参考文献：
    https://www.liujiangblog.com/course/django/158
    """

    # 列表显示
    list_display = (
        "created",
        "updated",
    )
    # 每页显示数据
    list_per_page = 10
    # 多筛选项
    list_filter = ("created", "updated")
    # 空值显示
    empty_value_display = "N/A"
