from django.shortcuts import render
from django.views import View

from .models import Cart
from eCommerce.products.models import Product
# Create your views here.
class CartsBaseView(View):
        
        def __init__(self):
            self.context = {}
            self.cart_obj = Cart.objects

class Carts(CartsBaseView):
    
    def get(self,request):
        """
        Method to update th user's carts whenever the user add an item to the 
        cart
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
            product_id = request.POST.get('product_id')
            if product_id:
                product_obj = Product().get_product_by_id(product_id)
                if not product_obj:
                    raise Product.DoesNotExist
                cart = self.cart_obj.get_or_create_cart(request)
                if product_obj in cart.products.all():
                    cart.products.remove(product_obj)
                else:
                    cart.products.add(product_obj)
                    request.session['cart_count'] = cart.products.count()
        except Exception as e:
            print("There was an issue updating the cart::%s" %(e.message))
