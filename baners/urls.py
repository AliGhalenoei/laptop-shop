from django.urls import path 
from .import views


urlpatterns = [
    path("header/",views.BanerHeaderAPIView.as_view()),
    path("home/pg/",views.BanerHomePageAPIView.as_view()),
]
