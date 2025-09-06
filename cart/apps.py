from django.apps import AppConfig


class CartConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cart'
    verbose_name = "سبد خرید کاربران"

    def ready(self):
        import cart.signals