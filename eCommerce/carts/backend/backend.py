
from ..models import Cart, CartDetails

class CartBackend():
    
    def __init__(self):
        self.context        = {}
        self.cart_obj       = Cart.objects
        self.cart_det_obj   = CartDetails.objects
        
    def updateCartWithUser(self,user, cart_id):
        try:
            if cart_id:
                cart_new = self.cart_obj.get_cart_by_id(cart_id)
                cart_old = self.cart_obj.get_cart_by_user(user)
                if cart_old:
                    cart_old_details = self.cart_det_obj.get_cart_items(cart_old.first().id)
                    for cod in cart_old_details:
                        cod.cart = cart_new.first()
                        cod.save()
                    cart_old.delete()
                cart_new.update(user=user)
        except:
            pass