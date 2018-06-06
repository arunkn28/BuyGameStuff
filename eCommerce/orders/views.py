from django.shortcuts import render
from django.views import View

from django.contrib.auth.models import User
from eCommerce.carts.models import Cart, CartDetails
# Create your views here.

class OrderViewBase(View):
    
    def __init__(self):
        self.cart_obj       = Cart.objects
        self.cart_det_obj   = CartDetails.objects
        self.context_dict   = {}

class OrderView(OrderViewBase):
    
    def get(self,request):
        cart            =   self.cart_obj.get_cart_by_user(request.user)
        cart_details    =   self.cart_det_obj.get_cart_items(cart.first().cart_id)
        self.context_dict['cart']           = cart.first()
        self.context_dict['cart_details']   = cart_details
        return render(request, 'order.html', self.context_dict)
        
    def post(self,request):
        pass
    
    
    