import json

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views import View
from django.http.response import HttpResponse

from .models import Cart, CartDetails
from ..products.models import Product

# Create your views here.
class CartsBaseView(View):
        
        def __init__(self):
            self.context        = {}
            self.cart_obj       = Cart.objects
            self.cart_det_obj   = CartDetails.objects

class CartView(CartsBaseView):
    
    def get(self,request):
        """
        View to show the cart page. Get the products in the cart base on whether the user is
        logged in or not.
        Think about the idea when user is logged in and not logged in.
        """
        try:
            if request.user.is_authenticated():
                cart = self.cart_obj.get_cart_by_user(request.user)
            else:
                cart = self.cart_obj.get_cart_by_id(request.session.get('cart_id',None)) 
            request.session['cart_id'] = cart.first().id
            cart_details_list =[]
            if cart:
                cart_details = self.cart_det_obj.get_cart_items(cart.first().id) 
                """ 
                :Note If face any issue with cart order by cartid and get the latest cartid.
                """
                for cart in cart_details:
                    product = Product.objects.filter(id=cart.product_id)
                    cart_temp_dict = {}
                    cart_temp_dict['product']       = product.first()
                    cart_temp_dict['quantity']      = cart.quantity
                    cart_temp_dict['price']         = product.first().price
                    cart_temp_dict[cart.id]         = cart.id
                    cart_details_list.append(cart_temp_dict)
                    
                self.context['cart_details'] = cart_details_list
                self.context['cart_count'] = cart_details.count()
            response = render(request, 'cart.html', self.context)
            return response
        except:
            print("500")
            raise Exception    
            
    def post(self,request):
        return redirect(reverse('order:orderview'))
    
    
class UpdateCart(CartsBaseView):
    """
    This the view which will get called on every addition or removal of
    product in the cart. Will update the cart based on the product id recieved from
    request
    """
    def post(self,request):
        try:
            product_id      = int(request.POST.get('product_id'))
            quantity        = request.POST.get('quantity')
            remove_product  = request.POST.get('remove_product')
            if product_id:
                if not remove_product: # Adding a product to cart
                    product_obj = Product.objects.get_product_by_id(product_id)
                    if not product_obj:
                        raise Product.DoesNotExist
                    cart = self.cart_obj.get_or_create_cart(request)
                    cart_detail_obj = self.cart_det_obj.get_cart_details(cart.id,product_id)
                    if cart_detail_obj:
                        if quantity:
                            cart_detail_obj.first().quantity = quantity
                            cart_detail_obj.first().save()
                        else:
                            cart_detail_obj.first().quantity = cart_detail_obj.first().quantity+1
                            cart_detail_obj.first().save()
                    else:                                         #and product id update the quantity only
                        self.cart_det_obj.create_cart_details(cart,product_obj)#Else this the first time product is being added
                    return redirect("/")
                else: # For removing the product from the cart                    #Create an entry in cart details object
                    cart_detail_obj = self.cart_det_obj.get_cart_details(request.session.get('cart_id'),product_id)
                    cart_detail_obj.delete()
                    cart_count =  self.cart_det_obj.get_cart_count(request.session.get('cart_id')) 
                    return HttpResponse(json.dumps({'cart_count': cart_count}), content_type="application/json")     
        except Product.DoesNotExist:
            pass
        except Exception as e:
            print("There was an issue updating the cart::%s" %(e.message))
            pass


class GetCartCount(CartsBaseView):
     
    def get(self,request):
        cart_id = request.session.get('cart_id')
            
        if request.user.is_authenticated():
            cart = self.cart_obj.get_cart_by_user(request.user)
        else:
            cart = self.cart_obj.get_cart_by_id(cart_id)
        cart_count = self.cart_det_obj.filter(cart_id=cart.first().id).count() if cart else 0
        return HttpResponse(json.dumps({'cart_count': cart_count}), content_type="application/json")
