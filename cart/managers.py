from django.db import models

from .models import Cart , CartItem

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
