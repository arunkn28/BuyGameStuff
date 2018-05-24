from django.shortcuts import render
from django.views import View

from .models import Cart, CartDetailsManager
from eCommerce.products.models import Product
# Create your views here.
class CartsBaseView(View):
        
        def __init__(self):
            self.context = {}
            self.cart_obj = Cart.objects

class Carts(CartsBaseView):
    
    def get(self,request):
        """
        View to show the cart page. Get the products in the cart base on whether the user is
        logged in or not.
        Think about the idea when user is logged in and not logged in.
        """
        try:
            cart = self.cart_obj.get_or_create_cart(request)
            self.context['cart'] = cart
            response = render(request, 'cart.html', self.context)
#             if not request.COOKIES.get('cart_id',None):
#                 response.set_cookie('cart_id', cart.id)
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
            product_id      = request.POST.get('product_id')
            quantity        = request.POST.get('quantity')
            remove_product  = request.POST.get('remove_product')
            if product_id:
                if not remove_product:
                    product_obj = Product().get_product_by_id(product_id)
                    if not product_obj:
                        raise Product.DoesNotExist
                    cart = self.cart_obj.get_or_create_cart(request)
                    cart_detail_obj = CartDetailsManager().get_cart_details(cart_id = cart.id,product_id)
                    if cart_detail_obj:
                        cart_detail_obj.update(quantity=quantity)
                    else:
                        CartDetailsManager().create_cart_details(cart_id = cart.id,product_id)
                else:
                    cart_detail_obj = CartDetailsManager().get_cart_details(cart_id = request.session.get('cart_id'),product_id)
                    cart_detail_obj.delete()       
                request.session['cart_count'] = CartDetailsManager().get_cart_count(cart_id = cart.id)
        except Product.DoesNotExist:
            pass
        except Exception as e:
            print("There was an issue updating the cart::%s" %(e.message))
            pass
