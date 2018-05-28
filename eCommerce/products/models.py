from django.db import models
from django.db.models.signals import pre_save
from django.db.models import Q

from django.urls import reverse

from eCommerce.utils import unique_slug_generator
from .utils import  CATEGORY_NAMES
                    
# Create your models here.

class Category(models.Model):
    """Category Table Schema"""

    name                    = models.CharField(choices=CATEGORY_NAMES,max_length=10)
    description             = models.TextField(max_length=100)
    image                   = models.ImageField(default=None,blank=True)
    created_by              = models.CharField(max_length=50,default=None)
    created_datetime        = models.DateTimeField(auto_now_add=True)
    modified_by             = models.CharField(max_length=50,null=True,default=None,blank=True)
    modified_datetime       = models.DateTimeField(null=True,blank=True,auto_now=True)
    
    def __str__(self):
        return u"%s" % (self.get_name_display())


class ProductManager(models.Manager):
    
    def get_product_by_id(self,product_id):
        product =  self.get_queryset().filter(pk=product_id)
        if product.count()== 1:
            return product.first()
        else:
            return None

    def get_products_by_feature(self,featured):
        """Method to get all featured products"""
        try:
            products = self.filter(featured=featured)
        except Product.DoesNotExist:
            products = None
        except:
            print('500')
            raise Exception        
        return products
    
    def get_product_by_slug(self,slug):
        """Method to get the product based on slug"""
        try:
            product =  self.get(slug=slug)
        except Product.DoesNotExist:
            raise Product.DoesNotExist
        except:
            print('500')
            raise Exception 
        return product
    
    def get_product_by_search(self,query):
        """Get the prodcuts based on serach"""
        try:
            search = Q(name__icontains=query)|Q(description__icontains=query)
            result = self.filter(search).distinct()
        except:
            print('500')
            raise Exception
        return result            
            
class Product(models.Model):
    """
    Product Table Schema
    Maybe make a new table to have offers on the products,i.e, discount, 
    coupon codes maybe?!
    Also check on adding extra image field for a product. 
    Will require 3-4 images each product and have to check an
    efficient way of doing that
    """
    sku                 = models.CharField(max_length=50,default=None)
    name                = models.CharField(max_length=200,default=None)
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
    created_datetime    = models.DateTimeField(auto_now_add=True)
    modified_by         = models.CharField(max_length=50,null=True,default=None,blank=True)
    modified_datetime   = models.DateTimeField(null=True,blank=True,auto_now=True)
    
    objects             = ProductManager()
    
    def get_absolute_url(self):
        return reverse("product:productdetails",kwargs={'slug':self.slug})
    
    def __str__(self):
        return self.name        
    
def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    
pre_save.connect(product_pre_save_receiver, sender=Product)        