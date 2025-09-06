from django.contrib import admin
from .models import Cart , CartItem
# Register your models here.


class CartItemInlines(admin.TabularInline):
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInlines]
    list_display = ["id"]

