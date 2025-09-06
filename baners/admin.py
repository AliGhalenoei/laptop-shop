from django.contrib import admin
from .models import BanerHeader , BanerHomePage
from django.utils.safestring import mark_safe
# Register your models here.


@admin.register(BanerHeader)
class BanerHeaderAdmin(admin.ModelAdmin):
    list_display = ["show_baner"]

    @mark_safe
    def show_baner(self, obj):
        return f'<img src="{obj.baner.url}" height="40px" width="50px" />'

@admin.register(BanerHomePage)
class BanerHeaderAdmin(admin.ModelAdmin):
    list_display = ["show_baner"]

    @mark_safe
    def show_baner(self , obj):
        return f'<img src="{obj.baner.url}" height="40px" width="50px" />'

