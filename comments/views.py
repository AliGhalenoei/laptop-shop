from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType

from products.models import Product
from .models import Comment
from .serializers import AddCommentSerializer ,CommentSerializer
# Create your views here.



class CreateCommentBaseAPIView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = AddCommentSerializer
    model = None

    def post(self , request , obj_id):
        object_instance = self.model.objects.get(id = obj_id)
        content_type = ContentType.objects.get_for_model(object_instance)
        serializer_data = self.serializer_class(data =request.data)

        if serializer_data.is_valid():
            message = serializer_data.validated_data["message"]
            Comment.objects.create(
                user = request.user,
                message = message,
                object_id = object_instance.id,
                content_type = content_type
            )
            return Response({"message":"کامنت با موفقیت اضافه شد"} , status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateCommentProductAPIView(CreateCommentBaseAPIView):

    """
        کامنت گزاشتن برای محصولات
        کاربر حتما باید لاگین باشد
    """

    model = Product

# class CreateCommentBlogAPIView(CreateCommentBaseAPIView):

#     """
#         کامنت گزاشتن برای بلاگ
#         کاربر حتما باید لاگین باشد
#     """

#     model = Blog


class BaseCommentsAPIView(APIView):

    serializer_class = CommentSerializer
    model = None

    def get(self , request , obj_id):
        object_instance = self.model.objects.get(id = obj_id)
        com = object_instance.comments.all()
        srz_data = self.serializer_class(instance = com , many = True)
        return Response(data=srz_data.data , status=status.HTTP_200_OK)
    
class CommentsProductAPIView(BaseCommentsAPIView):

    """
        لیست کامنت هایی که برای یک محصول گزاشتن
    """

    model = Product

# class CommentsBlogAPIView(BaseCommentsAPIView):
#     model = Blog


