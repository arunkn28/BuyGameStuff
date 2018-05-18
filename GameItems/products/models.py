from django.db import models

# Create your models here.

class Product(models.Model):
    """Product Table Schema"""
    product_sku             = models.CharField(max_length=50)
    product_title           = models.CharField(max_length=120)
    product_description     = models.TextField()
    category_id             = models.CharField(max_length=50)
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
    