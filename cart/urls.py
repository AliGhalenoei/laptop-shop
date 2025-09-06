from django.urls import path 
from .import views


urlpatterns = [
    path("items/",views.CartAPIView.as_view()),
    path("add/<int:product_id>/",views.AddCartAPIView.as_view()),
    path("remove/<int:item_id>/",views.RemoveCartAPIView.as_view()),
    path("sub/qu/<int:item_id>/",views.SubtractQuanttyCartAPIView.as_view()),
    path("add/qu/<int:item_id>/",views.AddQuanttyCartAPIView.as_view()),
    path("clear/",views.ClearCartAPIView.as_view()),
]
