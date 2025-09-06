from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import BanerHomePage , BanerHeader
from .serializers import BanerHeaderSerializer , BanerHomePageSerializer
# Create your views here.


class BanerHeaderAPIView(APIView):

    "عکس های اسلایدر هدر سایت"

    serializer_class = BanerHeaderSerializer

    def get(self , request):
        baners = BanerHeader.objects.order_by("-id")[:6]
        serializer_data = self.serializer_class(instance = baners , many = True)
        return Response(data=serializer_data.data , status=status.HTTP_200_OK)
    

class BanerHomePageAPIView(APIView):

    "عکس های اسلایدر صفحه خانه سایت"

    serializer_class = BanerHeaderSerializer

    def get(self , request):
        baners = BanerHeader.objects.order_by("-id")[:6]
        serializer_data = self.serializer_class(instance = baners , many = True)
        return Response(data=serializer_data.data , status=status.HTTP_200_OK)

