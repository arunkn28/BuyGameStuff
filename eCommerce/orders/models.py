from django.db import models
from django.db.models.signals import pre_save

from eCommerce.carts.models import Cart
from eCommerce.utils import generate_order_id
# Create your models here.
from .utils import ORDER_STATUS

class Order(models.Model):
    """
    User Id/Account ID key
    address key
    
    """
    orderid             = models.CharField(max_length=100,blank=True)
    status              = models.CharField(default='created',choices = ORDER_STATUS)
    cart                = models.ForeignKey(Cart)
    subtotal            = models.DecimalField(max_digits=7,decimal_places=2,default=0.00)
    total               = models.DecimalField(max_digits=7,decimal_places=2,default=0.00)
    created_by          = models.CharField(max_length=50)
    created_datetime    = models.DateField(auto_now=True)
    modified_by         = models.DateField(max_length=50)
    modified_datetime   = models.DateField(auto_now=True)


def pre_save_order_id(sender,instance,*args,**kwargs):
    if not instance.orderid:
        instance.orderid = generate_order_id(instance)    
    
pre_save.connect(pre_save_order_id, sender=Order)    