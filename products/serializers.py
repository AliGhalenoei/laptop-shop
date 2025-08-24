from rest_framework import serializers
from .models import Category , Product , GaleryProduct


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id" , "title" , "slug" , "sub_category" , "is_sub")


class GaleryProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = GaleryProduct
        fields = ("image",)

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only = True , many = True)
    galery = serializers.SerializerMethodField()

    class Meta:
        model = Product
        exclude = ("created" , "updated")

    def get_galery(self ,obj):
        result = obj.galerys.all()
        print("=====",result)
        return GaleryProductSerializer(instance = result , many = True).data
