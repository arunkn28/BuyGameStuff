from django.db import models
from django.db.models.signals import pre_save

from django.urls import reverse

from .utils import CATEGORY_PC, CATEGORY_PS3, CATEGORY_PS4, \
                    CATEGORY_XBOX1, unique_slug_generator 
                    
                    
                    
# Create your models here.

class Category(models.Model):
    """Category Table Schema"""

    CATEGORYNAMES = (
                    (CATEGORY_PS4,'PS4'),
                    (CATEGORY_PS3,'PS3'),
                    (CATEGORY_PC,'PC'),
                    (CATEGORY_XBOX1,'XBOX1')
                )
    name                    = models.CharField(choices=CATEGORYNAMES,max_length=10)
    description             = models.TextField(max_length=100)
    image                   = models.ImageField(default=None,blank=True)
    created_by              = models.CharField(max_length=50,default=None)
    created_datetime        = models.DateTimeField(default=None)
    modified_by             = models.CharField(max_length=50,null=True,default=None,blank=True)
    modified_datetime       = models.DateTimeField(null=True,default=None,blank=True)
    
    def __str__(self):
        return u"%s" % (self.get_name_display())


class ProductManager(models.Manager):
    def get_product_by_id(self,product_id):
        product =  self.get_queryset().filter(pk=product_id)
        if product.count()== 1:
            return product.first()
        else:
            return None

            
class Product(models.Model):
    """Product Table Schema"""
    sku                 = models.CharField(max_length=50,default=None)
    name                = models.CharField(max_length=120,default=None)
    description         = models.TextField(default=None)
    image               = models.ImageField(default=None,blank=True)
    featured            = models.BooleanField(default=False)
    slug                = models.SlugField(blank=True,unique=True,null=True)
    category_id         = models.ForeignKey(Category,default=None)
    quntity_per_unit    = models.IntegerField(default=None)
    price               = models.DecimalField(decimal_places=2,max_digits=7,default=0.00)
    weight              = models.DecimalField(decimal_places=2,max_digits=7,default=0.00)
    units_in_stock      = models.IntegerField(default=None)
    created_by          = models.CharField(max_length=50,default=None)
    created_datetime    = models.DateTimeField(default=None)
    modified_by         = models.CharField(max_length=50,null=True,default=None,blank=True)
    modified_datetime   = models.DateTimeField(null=True,default=None,blank=True)
    
    objects = ProductManager()
    
    def get_absolute_url(self):
        return reverse("productdetails",kwargs={'slug':self.slug})
    
    def __str__(self):
        return self.name        
    
def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    
pre_save.connect(product_pre_save_receiver, sender=Product)        