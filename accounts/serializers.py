from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# information jwt
class CustomClaimToken(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['phone'] = user.phone
        token['username'] = user.username
        token['is_active'] = user.is_active
        token['is_admin'] = user.is_admin
        token['is_superuser'] = user.is_superuser
        # ...

        return token

# registerition users
class UserRegisterSerializer(serializers.Serializer):

    """
        Step 1 register
    """

    phone = serializers.CharField(max_length = 11 , min_length = 11)

    def validate_phone(self , value):
        if User.objects.filter(phone = value).exists():
            raise serializers.ValidationError("تلفن همراه از قبلا ثبت نام کرده است")
        return value
    
class UserRegisterVerifySerializer(serializers.Serializer):

    """
        Step 2 register
    """

    code = serializers.IntegerField()

class UserRegisterCompleteSerializer(serializers.Serializer):

    """
        Step 3 register (final)
    """

    email  = serializers.EmailField(required = False)
    username = serializers.CharField()
    password = serializers.CharField()
    password2 = serializers.CharField()

    def validate(self, attrs):
        if attrs["password"] and attrs["password2"] and attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("رمز ها با هم مطابقت ندارد")
        return super().validate(attrs)

# Logout users
class UserLogoutSerializer(serializers.Serializer):

    """
        Logout User
    """

    refresh = serializers.CharField()