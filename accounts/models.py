from django.db import models
from django.contrib.auth.models import PermissionsMixin , AbstractBaseUser
from django.core.exceptions import ValidationError
import re
from django.core.validators import validate_integer
from .managers import UserManager
# Create your models here.


def valid_phone_ir(value):
    pattern = r'^09\d{9}$'
    if not re.match(pattern , value):
        raise ValidationError("شماره تلفن نامعتبر است")
    
class User(PermissionsMixin , AbstractBaseUser):
    phone = models.CharField(max_length=11 , unique=True  ,db_index=True ,verbose_name="تلفن همراه" , validators=[valid_phone_ir])
    email = models.EmailField(max_length=50 , unique=True , null=True , blank=True , verbose_name="ایمیل")
    username = models.CharField(max_length=60 , verbose_name="نام کاربری")

    is_active = models.BooleanField(default=True , verbose_name="کاربر فعال")
    is_admin = models.BooleanField(default=False , verbose_name="کاربر ادمین")
    created = models.DateTimeField(auto_now_add=True , verbose_name="کاربر مدیر")

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["email" , "username"]

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj = None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    

class OTP(models.Model):
    phone = models.CharField(max_length=11)
    code = models.SmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.code)
    
    def save(self, *args , **kwargs):
        exist_otp = OTP.objects.filter(phone = self.phone)
        if exist_otp.exists():
            exist_otp.delete()
        return super().save(*args , **kwargs)
