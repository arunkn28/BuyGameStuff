from django.db import models
from django.template.defaultfilters import default

# Create your models here.

class Category(models.Model):
    """Category Table Schema"""
    CATEGORY_PS4 = 'PS4'
    CATEGORY_PS3 = 'PS3'
    CATEGORY_PC  = 'PC'
    CATEGORY_XBOX1 = 'XBOX1'
    CATEGORYNAMES = (
                    (CATEGORY_PS4,'PS4'),
                    (CATEGORY_PS3,'PS3')
                    (CATEGORY_PC,'PC'),
                    (CATEGORY_XBOX1,'XBOX1')
                )
    category_name           = models.IntegerField(choices=CATEGORYNAMES)
    category_description    = models.TextField(max_length=100)
    category_image          = models.ImageField(default=None,blank=True)
    created_by              = models.CharField(max_length=50,default=None)
    created_datetime        = models.DateTimeField(default=None)
    modified_by             = models.CharField(max_length=50,null=True,default=None,blank=True)
    modified_datetime       = models.DateTimeField(null=True,default=None,blank=True)
    
    def __str__(self):
        return u"%s" % (self.get_category_name_display())

    
class Product(models.Model):
    """Product Table Schema"""
    product_sku             = models.CharField(max_length=50,default=None)
    product_title           = models.CharField(max_length=120,default=None)
    product_description     = models.TextField(default=None)
    product_image           = models.ImageField(default=None,blank=True)
    category_id             = models.ForeignKey(Category,default=None)
    quntity_per_unit        = models.IntegerField(default=None)
    product_price           = models.DecimalField(decimal_places=2,max_digits=7,default=0.00)
    product_weight          = models.DecimalField(decimal_places=2,max_digits=7,default=0.00)
    units_in_stock          = models.IntegerField(default=None)
    created_by              = models.CharField(max_length=50,default=None)
    created_datetime        = models.DateTimeField(default=None)
    modified_by             = models.CharField(max_length=50,null=True,default=None,blank=True)
    modified_datetime       = models.DateTimeField(null=True,default=None,blank=True)
    
    def __str__(self):
        return self.product_title        