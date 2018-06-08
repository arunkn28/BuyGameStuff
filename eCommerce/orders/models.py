from math import fsum

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User

from ..carts.models import Cart
from ..utils import generate_order_id
from ..products.models import Product
# Create your models here.
from .utils import ORDER_STATUS

class OrderManager(models.Manager):
    
    def get_order_or_create_by_cart(self,cart_id):
        return self.get_or_create(cart_id=cart_id)


class Order(models.Model):
    """
    User Id/Account ID key
    address key
    
    """
    orderid             = models.CharField(max_length=100,blank=True)
    status              = models.CharField(default='created', choices = ORDER_STATUS, max_length=10)
    user                = models.ForeignKey(User)
    cart                = models.ForeignKey(Cart)
    subtotal            = models.DecimalField(max_digits=7,decimal_places=2,default=0.00)
    total               = models.DecimalField(max_digits=7,decimal_places=2,default=0.00)
    created_by          = models.CharField(max_length=50,default='AK')
    created_datetime    = models.DateField(auto_now_add=True)
    #modified_by         = models.DateField(max_length=50,null=True)
    modified_datetime   = models.DateField(auto_now=True)
    
    objects             = OrderManager()


class OrderDetailsManager(models.Model):
    pass


class OrderDetails(models.Model):
    order               = models.ForeignKey(Cart)
    product             = models.ForeignKey(Product)
    price               = models.DecimalField(max_digits=7,decimal_places=2,default=0.00)
    quantity            = models.IntegerField(default=1)
    total               = models.DecimalField(max_digits=7,decimal_places=2,default=0.00)
    created_datetime    = models.DateField(auto_now_add=True)
    modified_datetime   = models.DateField(auto_now=True)
    
    objects             = OrderDetailsManager()
    
    def __str__(self):
        return str(self.order_id)

def pre_save_order_id(sender,instance,*args,**kwargs):
    if not instance.orderid:
        instance.orderid = generate_order_id(instance)    
    
pre_save.connect(pre_save_order_id, sender=Order)    

def post_save_order_details(sender,instance,*args,**kwargs):
    if instance.orderid:
        total=0
        total = fsum([total,instance.price*instance.quantity])
        instance.update(total=total)
    
post_save.connect(post_save_order_details, sender=OrderDetails)    


class OrderHistoryManager(models.Manager):
    pass
    
class OrderHistory(models.Model):
    """
    Whenver a order changes status that will be added/updated to this table
    """
    orderid             = models.CharField(max_length=100,blank=True)
    status              = models.CharField(default='created', choices = ORDER_STATUS, max_length=10)
    user                = models.ForeignKey(User)
    cart                = models.ForeignKey(Cart)
    subtotal            = models.DecimalField(max_digits=7,decimal_places=2,default=0.00)
    total               = models.DecimalField(max_digits=7,decimal_places=2,default=0.00)
    created_by          = models.CharField(max_length=50)
    created_datetime    = models.DateField(auto_now_add=True)
    #modified_by         = models.DateField(max_length=50)
    modified_datetime   = models.DateField(auto_now=True)
    
    objects             = OrderHistoryManager()
