from django.shortcuts import render
from django.views import View

from django.contrib.auth.models import User
from ..carts.models import Cart, CartDetails
from .models import Order, OrderDetails
from ..account.utils import STATE_MAPPING
# Create your views here.

class OrderViewBase(View):
    
    def __init__(self):
        self.cart_obj       = Cart.objects
        self.cart_det_obj   = CartDetails.objects
        self.order_obj      = Order.objects
        self.order_det_obj  = OrderDetails.objects
        self.context_dict   = {}

class OrderView(OrderViewBase):
    
    def get(self,request):
        try:
            cart            =   self.cart_obj.get_cart_by_user(request.user)
            cart_details    =   self.cart_det_obj.get_cart_items(cart.first().id)
            self.context_dict['cart']           = cart.first()
            self.context_dict['cart_details']   = cart_details
            self.context_dict['states'] = STATE_MAPPING
            return render(request, 'order.html', self.context_dict)
        except Exception as e:
            print("500")
            raise e
            
    def post(self,request):
        """
        Create an order with status as Created
        Check if already an order exists in created status for this user.
        If exists :
        update the order with the new cart items 
        else:
        create an order
        """
        try:
            cart            =   self.cart_obj.get_cart_by_user(request.user)
            cart_details    =   self.cart_det_obj.get_cart_items(cart.first().id)
            order           =   self.order_obj.get_order_or_create_by_cart(cart_id=cart.first().id,user_id=request.user)
            for item in cart_details:
                order_det   =   self.order_det_obj.get_cart_det_or_create(order.first().id,item.product.id)
                order_det.first().price = item.price
                order_det.first().quantity = item.quantity
                order_det.first().save()
            """
                Code for instamojo payment
            """
        except Exception as e:
            raise e
                
    
    
    