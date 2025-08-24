from django.urls import path 
from .import views


urlpatterns = [
    path("categorys/",views.CategoryAPIView.as_view()),
    path("",views.ProductAPIView.as_view()),
    path("<slug:slug_product>/",views.RetrieveProductAPIView.as_view()),
]
