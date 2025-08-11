from django.urls import path 
from .import views
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView


urlpatterns = [
    # register paths
    path("register/",views.UserRegisterAPIView.as_view()),
    path("register/verify/",views.UserRegisterVerifyAPIView.as_view()),
    path("register/complete/",views.UserRegisterCompleteAPIView.as_view()),
    # login paths
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/refresh/', TokenRefreshView.as_view()),
    # logout path
    path('logout/', views.UserLogoutAPIView.as_view()),
]
