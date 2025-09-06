from django.db.models.signals import post_save
from accounts.models import User
from cart.models import Cart


def create_cart_user(sender , *args , **kwargs):
    if kwargs["created"]:
        Cart.objects.create(user = kwargs["instance"])
        return True

post_save.connect(create_cart_user , sender=User)