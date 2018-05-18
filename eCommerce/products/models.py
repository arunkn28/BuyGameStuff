from django.db import models

# Create your models here.

CATEGORYNAMES = ((0,'PS4'),
                 (1,'PC'))

class Category(models.Model):
    """Category Table Schema"""
    category_name           = models.CharField(max_length=50,choices=CATEGORYNAMES)
    category_description    = models.TextField(max_length=100)
    category_image          = models.ImageField()
    created_by              = models.CharField(max_length=50)
    created_datetime        = models.DateTimeField()
    modified_by             = models.CharField(max_length=50)
    modified_datetime       = models.DateTimeField()
    
    def __Str__(self):
        return self.category_name

    
class Product(models.Model):
    """Product Table Schema"""
    product_sku             = models.CharField(max_length=50)
    product_title           = models.CharField(max_length=120)
    product_description     = models.TextField()
    product_image           = models.ImageField()
    category_id             = models.ForeignKey(Category)
    quntity_per_unit        = models.IntegerField()
    product_price           = models.DecimalField()
    product_weight          = models.DecimalField()
    units_in_stock          = models.IntegerField()
    created_by              = models.CharField(max_length=50)
    created_datetime        = models.DateTimeField()
    modified_by             = models.CharField(max_length=50)
    modified_datetime       = models.DateTimeField()
    
    def __str__(self):
        return self.title        