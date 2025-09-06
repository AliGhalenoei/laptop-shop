from rest_framework import serializers
from .models import Cart , CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = CartItem
        fields = ("id","quantity","product")

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True , read_only = True)

    class Meta:
        model = Cart
        fields = ("user","session_key" , "items")

class AddCartSerializer(serializers.Serializer):
    quantity = serializers.IntegerField()

