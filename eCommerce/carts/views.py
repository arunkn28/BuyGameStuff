from django.shortcuts import render, redirect
from django.views import View

from .models import Cart, CartDetails
from eCommerce.products.models import Product
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
            
            cart_details = self.cart_det_obj.get_cart_items(cart.first().id)
            self.context['cart_details'] = cart_details
            response = render(request, 'cart.html', self.context)
            return response
        except:
            print("500")
            raise Exception    
            

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
                            cart_detail_obj.update(quantity=quantity) #If in cartdetails already exists for given cattid
                        else:
                            cart_detail_obj.update(quantity=cart_detail_obj.first().quantity+1)
                    else:                                         #and product id update the quantity only
                        self.cart_det_obj.create_cart_details(cart,product_obj)#Else this the first time product is being added
                else: # For removing the product from the cart                    #Create an entry in cart details object
                    cart_detail_obj = self.cart_det_obj.get_cart_details(request.session.get('cart_id'),product_id)
                    cart_detail_obj.delete()       
                request.session['cart_count'] = self.cart_det_obj.get_cart_count(request.session.get('cart_id'))
                return redirect("/")
        except Product.DoesNotExist:
            pass
        except Exception as e:
            print("There was an issue updating the cart::%s" %(e.message))
            pass


"""
Ajax call to get the count of items in cart.
Before getting count get the cart_id form session, if exists,
1. Get the last cart details for this user and update the new cart details with that aong with user
and delete the previous records of cart and cart details 
2. If last cart not available update the user for the present cart

if No cart id exists in session
1. Get cart count for this user
"""
# class GetCartCount(CartsBaseView):
#     
#     def post(self,request):
#         user = request.user
#         cart_id = request.session.get('cart_id')
        
    