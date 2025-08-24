from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from .models import *
from .serializers import *
# Create your views here.



class CategoryAPIView(APIView):

    """
        گرفتن تمام دسته بندی های اصلی
    """

    serializer_class = CategorySerializer

    def get(self , request):
        category = Category.objects.filter(is_sub = False)
        serializer_data = self.serializer_class(instance = category , many = True)
        return Response(data=serializer_data.data , status=status.HTTP_200_OK)
    
    
class ProductAPIView(APIView):

    """
        گرفتن تمام محصولات موجود
    """

    serializer_class = ProductSerializer

    def get(self , request):
        products = Product.objects.filter(is_available = True)
        serializer_data = self.serializer_class(instance = products , many = True)
        return Response(data=serializer_data.data , status=status.HTTP_200_OK)
    

class RetrieveProductAPIView(APIView):

    """
        گرفتن جزییات یک محصول \n
        باید اسلاگ محصول وارد آدرس بشه
    """

    serializer_class = ProductSerializer

    def get(self , request , slug_product):
        try:
            product = Product.objects.get(slug = slug_product)
            serializer_data = self.serializer_class(instance = product)
            return Response(data=serializer_data.data , status=status.HTTP_200_OK)
        except:
            return Response({"message":"Page Not Found"} , status=status.HTTP_404_NOT_FOUND)


