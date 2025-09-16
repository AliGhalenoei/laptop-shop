from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
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
        

class BookmarkProductAPIView(APIView):
    
    """
        افزودن به علاقه مندی ها
    """

    permission_classes = [IsAuthenticated]

    def get(self , request , product_id):
        product_instance = Product.objects.get(id = product_id)
        check = Bookmark.objects.filter(user = request.user , product = product_instance)
        if check.exists():
            bookmark = Bookmark.objects.get(user = request.user , product = product_instance).delete()
            return Response({
                "message":f"محصول  از علاقه مندی ها حذف شد"
            }, status=status.HTTP_200_OK)
        else:
            bookmark = Bookmark.objects.create(user = request.user , product = product_instance)
            return Response({
                "message":f"محصول {bookmark.product.title} به علاقه مندی ها اضافه شد"
            }, status=status.HTTP_200_OK)

class bookmarksUserAPIView(APIView):
    
    """
        لیست علاقه مندی های کاربر
    """

    permission_classes = [IsAuthenticated]
    serializer_class = BookmarkSerializer

    def get(self , request ):
        products = request.user.bookmarks.all()
        serializer_data = self.serializer_class(instance = products , many = True)
        return Response(data=serializer_data.data,status=status.HTTP_200_OK)
    
class SuggestedProductAPIView(APIView):

    """
        محصولات مرتبط
    """

    serializer_class = ProductSerializer

    def get(self , request , product_id):
        product = Product.objects.get(id = product_id)
        category = product.category.filter(is_sub = False).first()
        suggested_products =Product.objects.filter(category = category).order_by("-id").exclude(id = product.id)[:10]
        serializer_data = self.serializer_class(instance = suggested_products , many = True)
        return Response(data=serializer_data.data , status=status.HTTP_200_OK)

