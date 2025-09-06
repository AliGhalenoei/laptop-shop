from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import *
# Register your models here.



@admin.register(Category)
class CategorAdmin(admin.ModelAdmin):
    list_display = ["show_baner","title" , "is_sub"]
    fields =["title" , "slug" , "sub_category", "image"]

    @mark_safe
    def show_baner(self , obj):
        return f'<img src="{obj.image.url}" height="20px" width="30px" />'

class GaleryProductInlines(admin.TabularInline):
    model = GaleryProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (GaleryProductInlines,)
    list_display = ["show_baner" , "title" , "is_available" , "stock"]
    filter_horizontal = ["category"]
    # filter_vertical = ["category"]
    exclude = ["discount_off"]

    @mark_safe
    def show_baner(self , obj):
        return f'<img src="{obj.baner.url}" height="20px" width="30px" />'
