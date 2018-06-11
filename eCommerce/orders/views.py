from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from ..account.utils import STATE_MAPPING
from ..carts.models import Cart, CartDetails
from ..account.models import AccountAddress, Account

from .models import Order, OrderDetails

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
            #Make changes to get userid and account from session
            user                                =   User.objects.filter(username=request.user)
            account                             =   Account.objects.get_account_by_user(user.first().id)
            address_details                     =   AccountAddress.objects.seacrh_address_by_account(account.first().id)
            cart                                =   self.cart_obj.get_cart_by_user(request.user)
            cart_details                        =   self.cart_det_obj.get_cart_items(cart.first().id)
            self.context_dict['cart']           =   cart.first()
            self.context_dict['cart_details']   =   cart_details
            self.context_dict['states']         =   STATE_MAPPING
            self.context_dict['address_details']=   address_details.first()
            return render(request, 'order.html', self.context_dict)
        except Exception as e:
            print("500")
            raise e
            
    def post(self,request):
        """
        :NOTE:: Check that the quantity of items is available 
        If not available show a message saying that the available quantity is x,
        and update the quantity with x
        Also on successfull completion of payment subtract the quntity in
        the product table
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
            order, created  =   self.order_obj.get_order_or_create_by_cart(cart.first().id,request.user,'created')
            for item in cart_details:
                order_det,created           = self.order_det_obj.get_order_det_or_create(order.id,item.product.id)
                order_det.price             = item.price
                order_det.quantity          = item.quantity
                order_det.save()
            """
                Code for instamojo payment
            """
            return HttpResponseRedirect("/")
        except Exception as e:
            raise e
                
    
    
    