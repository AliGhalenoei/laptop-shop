from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FAQ , AboutUs , ContactUs
from .serializers import FAQSerializer , ContactSerializer , AboutSerializer
# Create your views here.


class FAQ_APIView(APIView):

    """
        سوالات متداول
    """

    serializer_class = FAQSerializer

    def get(self , request):
        faqs = FAQ.objects.all()
        serializer_data = self.serializer_class(instance = faqs , many = True)
        return Response(data=serializer_data.data , status=status.HTTP_200_OK)
    
class ContactUsAPIView(APIView):

    """
        صفحه تماس با ما
    """

    serializer_class = ContactSerializer

    def get(self , request):
        faqs = ContactUs.objects.first()
        serializer_data = self.serializer_class(instance = faqs)
        return Response(data=serializer_data.data , status=status.HTTP_200_OK)
    
class AboutUsAPIView(APIView):

    """
        صفحه درباره ما
    """

    serializer_class = ContactSerializer

    def get(self , request):
        faqs = AboutUs.objects.first()
        serializer_data = self.serializer_class(instance = faqs)
        return Response(data=serializer_data.data , status=status.HTTP_200_OK)


