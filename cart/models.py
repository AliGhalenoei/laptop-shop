from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


from accounts.models import User
from products.models import Product 


class CartManager(models.Manager):
    def get_user_cart(self, request):
        """دریافت سبد خرید کاربر بر اساس وضعیت authentication"""
        if request.user.is_authenticated:
            cart, created = self.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            cart, created = self.get_or_create(
                session_key=session_key,
                user__isnull=True
            )
        return cart
    
    def merge_carts(self, request):
        """ادغام سبد خرید هنگام لاگین کاربر"""
        if request.user.is_authenticated:
            try:
                # پیدا کردن سبد خرید بر اساس session
                anonymous_cart = self.get(
                    session_key=request.session.session_key,
                    user__isnull=True
                )
                
                # پیدا کردن یا ایجاد سبد خرید کاربر
                user_cart, created = self.get_or_create(user=request.user)
                
                # ادغام آیتم‌ها
                for item in anonymous_cart.items.all():
                    try:
                        # اگر محصول در سبد کاربر وجود دارد
                        user_item = CartItem.objects.get(
                            cart=user_cart,
                            product=item.product,
                        )
                        user_item.quantity += item.quantity
                        user_item.save()
                    except CartItem.DoesNotExist:
                        # اگر محصول وجود ندارد، آیتم جدید ایجاد کن
                        item.cart = user_cart
                        item.save()
                
                # حذف سبد anonymous
                anonymous_cart.delete()
                
            except Cart.DoesNotExist:
                pass


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CartManager()

    class Meta:
        unique_together = ['user', 'session_key']
        verbose_name = "سبد خرید"
        verbose_name_plural = "سبد های خرید"
    
    def __str__(self):
        if self.user:
            return f"سبد خرید {self.user.username}"
        return f"سبد خرید ناشناس ({self.session_key})"
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    def add_product(self, product, quantity=1):
        """افزودن محصول به سبد خرید"""
        cart_item, created = CartItem.objects.get_or_create(
            cart=self,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return cart_item
    
    def remove_product(self, product):
        """حذف محصول از سبد خرید"""
        try:
            cart_item = CartItem.objects.get(cart=self, product=product)
            cart_item.delete()
            return True
        except CartItem.DoesNotExist:
            return False
    
    def clear(self):
        """خالی کردن سبد خرید"""
        self.items.all().delete()
    
    def get_cart_items(self):
        """دریافت تمام آیتم‌های سبد"""
        return self.items.select_related('product').all()


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cart', 'product']
        verbose_name = "آیتم های سبد خرید"
        verbose_name_plural = "آیتم"
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    def clean(self):
        """اعتبارسنجی موجودی محصول"""
        if self.quantity > self.product.stock:
            raise ValidationError(
                f"موجودی محصول {self.product.title} کافی نیست. "
                f"موجودی فعلی: {self.product.stock}"
            )
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)