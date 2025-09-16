from django.urls import path 
from .import views


urlpatterns = [
    path("product/add/<int:obj_id>/",views.CreateCommentProductAPIView.as_view()),
    path("products/<int:obj_id>/",views.CommentsProductAPIView.as_view()),
]
