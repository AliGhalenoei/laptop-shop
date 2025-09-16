from django.urls import path 
from .import views


urlpatterns = [
    path("faqs/",views.FAQ_APIView.as_view()),
    path("contactus/",views.ContactUsAPIView.as_view()),
    path("about/",views.AboutUsAPIView.as_view()),
]
