from django.db import models

from eCommerce.carts.models import Cart
# Create your models here.
from .utils import ORDER_STATUS

class Order(models.Model):
    """
    User Id/Account ID key
    address key
    
    """
    orderid             = models.CharField(max_length=100)
    status              = models.CharField(default='created',choices = ORDER_STATUS)
    cart                = models.ForeignKey(Cart)
    subtotal            = models.DecimalField(max_digits=7,decimal_places=2,default=0.00)
    total               = models.DecimalField(max_digits=7,decimal_places=2,default=0.00)
    