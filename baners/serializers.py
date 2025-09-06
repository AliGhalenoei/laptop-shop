from rest_framework import serializers
from .models import BanerHeader , BanerHomePage


class BanerHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = BanerHeader
        fields = ("baner" , "alt" , "link")

class BanerHomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BanerHomePage
        fields = ("baner" , "alt" , "link")

