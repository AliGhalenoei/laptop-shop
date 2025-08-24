from django.contrib import admin
from .models import *
# Register your models here.



@admin.register(Category)
class CategorAdmin(admin.ModelAdmin):
    list_display = ["title" , "is_sub"]

    fields =["title" , "slug" , "sub_category"]

class GaleryProductInlines(admin.TabularInline):
    model = GaleryProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (GaleryProductInlines,)
    list_display = ["title"]
    filter_horizontal = ["category"]
    # filter_vertical = ["category"]
    exclude = ["discount_off"]
