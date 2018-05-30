from django.db import models
from django.db.models.signals import pre_save
from django.contrib.auth.models import User

from eCommerce.carts.models import Cart
from eCommerce.utils import generate_order_id
# Create your models here.
from .utils import ORDER_STATUS

class OrderManager(models.Manager):
    pass


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
    created_by          = models.CharField(max_length=50)
    created_datetime    = models.DateField(auto_now_add=True)
    modified_by         = models.DateField(max_length=50)
    modified_datetime   = models.DateField(auto_now=True)
    
    objects             = OrderManager()

def pre_save_order_id(sender,instance,*args,**kwargs):
    if not instance.orderid:
        instance.orderid = generate_order_id(instance)    
    
pre_save.connect(pre_save_order_id, sender=Order)    


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
    modified_by         = models.DateField(max_length=50)
    modified_datetime   = models.DateField(auto_now=True)
    
    objects             = OrderHistoryManager()