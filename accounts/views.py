from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView 

import random
from .models import User , OTP
from .serializers import (
    UserRegisterSerializer,
    UserRegisterVerifySerializer,
    UserRegisterCompleteSerializer,
    UserLogoutSerializer,
    CustomClaimToken
)
from .kave_otp import send_otp


# Register User Steps
class UserRegisterAPIView(APIView):

    """
        رجیستر کردن کاربر (مرحله اول)
        تلفن کاربر را دریافت میکند و در سشن ذخیره میکند
    """

    serializer_class = UserRegisterSerializer

    def post(self , request):
       serializer_data = self.serializer_class(data = request.data)

       if serializer_data.is_valid():
           create_code_otp = random.randint(1000,9999)

           OTP.objects.create(phone = serializer_data.validated_data["phone"] , code = create_code_otp)
           send_otp(serializer_data.validated_data["phone"] , create_code_otp)
           request.session["user_phone_info"] = serializer_data.validated_data["phone"]
           return Response(
               {
                   "message":"یک کد به شماره تلفن ارسال شد . به صفحه تایید کد ریدایرکت شود",
                   "data":serializer_data.data
               },
               status=status.HTTP_302_FOUND
           )
       return Response(serializer_data.errors)
    
class UserRegisterVerifyAPIView(APIView):

    """
        رجیستر کردن کاربر (مرحله دوم)
        کد ارسال شده به تلفن همراه را دریافت میکند
    """

    serializer_class = UserRegisterVerifySerializer

    def post(self , request):
        get_session_user = request.session.get("user_phone_info")
        otp_user = OTP.objects.get(phone = get_session_user)
        serializer_data = self.serializer_class(data= request.data)

        if serializer_data.is_valid():
            if serializer_data.validated_data["code"] == otp_user.code:
                otp_user.delete()
                return Response(
                    {
                        "message":"کد تایید شد به مرحله نهایی ریدایرکت شود"
                    },
                    status=status.HTTP_302_FOUND
                )
            else:
                return Response(
                    {
                        "message":"کد معتبر نیست"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer_data.errors)
    
class UserRegisterCompleteAPIView(APIView):

    """
        رجیستر کردن کاربر (مرحله سوم)
        مرحله نهایی ثبت نام کاربر
        ایمیل و نام کاربری و رمزعبور را دریافت میکند و در نهایت کاربر رجیستر میشود و لاگین میشود
        و یک جفت توکن اکسس و رفرش دریافت میکند

        ارسال ایمیل اجباری نیست
    """

    serializer_class = UserRegisterCompleteSerializer

    def post(self , request):
        get_session_user = request.session.get("user_phone_info")
        serializer_data = self.serializer_class(data = request.data)

        if serializer_data.is_valid():
            vd = serializer_data.validated_data

            create_user = User.objects.create(
                phone =get_session_user,
                email = vd["email"],
                username = vd["username"],
                password = vd["password"]
            )

            refresh = RefreshToken.for_user(create_user)
            refresh["phone"] = create_user.phone
            refresh["username"] = create_user.username
            refresh["is_active"] = create_user.is_active
            refresh["is_admin"] = create_user.is_admin
            refresh["is_superuser"] = create_user.is_superuser

            access = refresh.access_token
            access["phone"] = create_user.phone
            access["username"] = create_user.username
            access["is_active"] = create_user.is_active
            access["is_admin"] = create_user.is_admin
            access["is_superuser"] = create_user.is_superuser

            return Response(
                {
                    "message":"کاربر ثبت نام شد",
                    "access-token":str(access),
                    "refresh-token":str(refresh)
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer_data.errors)

# Login User 
class UserLoginAPIView(TokenObtainPairView):
    
    """
        لاگین کردن کاربر 
        تلفن و رمزعبور را دریافت میکند و لاگین میشود 
        و ذر نهایت یک جفت توکن اکسس و رفرش برمیگرداند
    """

    serializer_class = CustomClaimToken

# Logout User
class UserLogoutAPIView(APIView):

    """
        خروج از حساب کاربری
        باید مقدار رفرش توکن کاربر رو براش ارسال کنید

        و بعدش اکسس توکن کاربر هم  از لوکال استورج یا هرجایی که ذخیره کردی حذف کنی
    """

    serializer_class = UserLogoutSerializer

    def post(self , request):
        serializer_data = self.serializer_class(data = request.data)

        if serializer_data.is_valid():
            RefreshToken(serializer_data.validated_data["refresh"]).blacklist()
            return Response(
                {
                    "message":"رفرش توکن کاربر منقضی شد"
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer_data.errors)