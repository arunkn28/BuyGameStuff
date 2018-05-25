from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, post_delete, pre_save
# Create your models here.
from math import fsum
from eCommerce.products.models import Product
User = settings.AUTH_USER_MODEL


class CartManager(models.Manager):
    
    def create_cart_obj(self,user):
        return self.create(user=user)
    
    def get_cart_by_id(self,cart_id):
        return self.get_queryset().filter(id=cart_id)
     
    def get_or_create_cart(self,request):
        cart_id = request.session.get('cart_id',None)
        qs = self.get_cart_by_id(cart_id)
        if qs.count()==1:
            cart_obj = qs.first()
            if request.user.is_authenticated() and not cart_obj.user:
                cart_obj.user = request.user
                cart_obj.save()
        else:        
            cart_obj = self.create_cart_obj(request.user)
            request.session['cart_id'] = cart_obj.id
        return cart_obj    
    
            
class Cart(models.Model):
    """
    Cart Model
    Create one more table to store the product quantity in cart.
    Should have a foreign key to cart and for each product in cart will have a
    record having the quantity.
    """
    user                = models.ForeignKey(User, null =True, blank=True)
    #products            = models.ManyToManyField(Product, blank=True)
    subtotal            = models.DecimalField(max_digits=7,decimal_places=2,default=0.00)
    total               = models.DecimalField(max_digits=7,decimal_places=2,default=0.00)
    created_datetime    = models.DateField(auto_now_add=True)
    modified_datetime   = models.DateField(auto_now=True)
    
    objects             = CartManager()
    
    def __str__(self):
        return str(self.id)

    
    
# def m2m_changed_cart_receiver(sender,instance,action,*args,**kwargs):
#     """
#     This is used to update the cart total whenever there is an addition or removal 
#     from the cart
#     """
#     if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
#         products = instance.objects.all()
#         total = 0
#         for product in products:
#             total += product.price
#         instance.subtotal = total
#         instance.save()
#         
# m2m_changed.connect(m2m_changed_cart_receiver, sender= Cart.products.through)            
#              

# def pre_save_cart_receiver(sender,instance,*args,**kwargs):
#     """
#     Add the extraCharges Method to take into consideration
#     the shipping charges and taxes
#     """
#     if instance.subtotal> 0.00:
#         instance.total = instance.subtotal #+ extraCharges()
#          
# pre_save.connect(pre_save_cart_receiver, sender=Cart)                    

class CartDetailsManager(models.Manager):
    
    def get_cart_details(self,cart_id,product_id):
        return self.filter(product_id=product_id,cart_id=cart_id)        
    
    def create_cart_details(self,cart,product):
        return self.create(cart=cart,product=product,price=product.price )
    
    def get_cart_count(self,cart_id):
        return self.get_queryset().filter(cart_id=cart_id).count()    
    
    def get_cart_items(self,cart_id):
        return self.get_queryset().filter(cart_id)
    
    
class CartDetails(models.Model):
    cart                = models.ForeignKey(Cart)
    product             = models.ForeignKey(Product)
    price               = models.DecimalField(max_digits=7,decimal_places=2,default=0.00)
    quantity            = models.IntegerField(default=1)
    created_datetime    = models.DateField(auto_now_add=True)
    modified_datetime   = models.DateField(auto_now=True)
    
    objects             = CartDetailsManager()
    
    def __str__(self):
        return str(self.cart_id)


"""
    Signals to update the total and subtotal in the Cart Details
"""    
def post_save_cart_details_receiver(sender,instance,*args,**kwargs):
    """
    Add the extraCharges Method to take into consideration
    the shipping charges and taxes
    """
    cart_details_obj = CartDetails.objects.filter(cart_id=instance.cart_id)
    if cart_details_obj:
        total = 0
        for cart in cart_details_obj:
            total = fsum([total,cart.price*cart.quantity])
        Cart.objects.filter(pk=instance.cart_id).update(subtotal=total,total=total)
            
post_save.connect(post_save_cart_details_receiver, sender=CartDetails)   
post_delete.connect(post_save_cart_details_receiver, sender=CartDetails)                   
