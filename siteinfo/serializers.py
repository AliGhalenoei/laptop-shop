from rest_framework import serializers
from .models import ContactUs , AboutUs , FAQ


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"

class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = "__all__"

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"





