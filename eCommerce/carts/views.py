from django.shortcuts import render
from django.views import View

# Create your views here.
class CartsBaseView(View):
        
        def __init__(self):
            self.context = {}
            self.cart_obj = Carts.objects

class Carts(CartsBaseView):
    
    def get(self,request):
        """Method to update th user's carts whenever the user add an item to the 
        cart"""
        try:
            cart = self.cart_obj.get_or_create_cart(request)
            self.context['cart'] = cart
            response = render(request, '', self.context)
#             if not request.COOKIES.get('cart_id',None):
#                 response.set_cookie('cart_id', cart.id)
            return response
        except:
            print("500")
            raise Exception    
            
    