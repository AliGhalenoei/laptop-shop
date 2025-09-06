from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Cart, CartItem
from .serializers import CartSerializer ,AddCartSerializer  
from products.models import Product


class CartAPIView(APIView):

    """نمایش سبد خرید"""

    serialzer_class = CartSerializer

    def get(self,request):
        cart = Cart.objects.get_user_cart(request)
        srz_data = self.serialzer_class(cart)
        response_data = {
            'cart': srz_data.data,
            'total_price': cart.total_price,
            'total_items': cart.total_items
        }
        return Response(data=response_data,status=status.HTTP_200_OK)

class AddCartAPIView(APIView):

    serializer_class = AddCartSerializer

    def post(self ,request, product_id):
        """افزودن محصول به سبد خرید"""

        srz_data = self.serializer_class(data = request.data)

        if srz_data.is_valid():
            vd = srz_data.validated_data
            product = get_object_or_404(Product, id=product_id)
                
            cart = Cart.objects.get_user_cart(request)
                
            try:
                cart_item = cart.add_product(product, vd["quantity"])
                return Response({
                        'success': True,
                        'message': 'محصول به سبد خرید اضافه شد',
                        'total_items': cart.total_items
                    },status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({
                        'success': False,
                        'message': str(e)
                    }, status=status.HTTP_400_BAD_REQUEST)
        return Response(srz_data.errors,status=status.HTTP_400_BAD_REQUEST)
        
class RemoveCartAPIView(APIView):

    def get(self ,request, item_id):
        """حذف محصول از سبد خرید"""
        cart = Cart.objects.get_user_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        cart_item.delete()
        
        return Response({
                'success': True,
                'message': 'محصول از سبد خرید حذف شد',
                'total_items': cart.total_items,
                'total_price': cart.total_price
            },status=status.HTTP_200_OK)
        
class SubtractQuanttyCartAPIView(APIView):
    """افزایش تعداد محصول در سبد"""
    def get(self , request, item_id):
        
        cart = Cart.objects.get_user_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        if cart_item.quantity <= 1:
            cart_item.delete()
            return Response({"message":"محصول حذف کامل شد"},status=status.HTTP_200_OK)
        else:
            cart_item.quantity-=1
            cart_item.save()
            return Response({"message":"از تعداد محصول یکی کم شد"},status=status.HTTP_200_OK)
            
class AddQuanttyCartAPIView(APIView):
    """کاهش تعداد محصول در سبد"""

    def get(self , request, item_id):
        cart = Cart.objects.get_user_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        if cart_item.quantity != cart_item.product.stock:
            cart_item.quantity+=1
            cart_item.save()
            return Response({"message":"یکی به تعدا سبد اضافه شد"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"بیشتر از این در انبار موجود نمیباشد"},status=status.HTTP_200_OK)

class ClearCartAPIView(APIView):
    """حذف کل سبد یکجا"""

    def get(self , request):
        cart = Cart.objects.get_user_cart(request)
        cart.clear()
        return Response({"message":"سبد خالی شد"})
    
    
# @login_required
# def checkout(request):
#     """صفحه تسویه حساب"""
#     cart = Cart.objects.get_user_cart(request)
    
#     if cart.total_items == 0:
#         return redirect('cart:cart_detail')
    
#     context = {
#         'cart': cart,
#         'cart_items': cart.get_cart_items()
#     }
#     return render(request, 'cart/checkout.html', context)