from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import User , OTP
from .forms import UserCreationForm , UserChangeForm
# Register your models here.


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["username" , "phone" , "email" , "is_active" , "is_admin" , "is_superuser" , "id"]
    list_filter = ["is_admin" , "is_superuser"]
    search_fields = ["username" , "email" , "phone"]
    filter_horizontal = ()
    ordering = ["id"]

    fieldsets = (
        ("اطلاعات کاربری" , {"fields":("phone","email","username","password")}),
        ("دسترسی ها" , {"fields":("is_active" , "is_admin" , "is_superuser")}),
    )

    add_fieldsets = (
        ("ساخت حساب کاربری" , {"fields":("phone","email","username","password" ,"password2")}),
    )
admin.site.unregister(Group)
admin.site.register(User , UserAdmin)


@admin.register(OTP)
class OtpAdmin(admin.ModelAdmin):
    list_display = ["phone" , "code"]
