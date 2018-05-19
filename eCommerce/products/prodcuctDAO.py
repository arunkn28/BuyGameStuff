from .models import Product, Category


class ProductDAO():
    
    def __init__(self):
        pass
    
    def get_products_by_feature(self,featured):
        """Method to get all featured products"""
        try:
            products = Product.objects.filter(featured=featured)
        except Product.DoesNotExist:
            products = None
        except:
            print('500')
            raise Exception        
        return products
    
    def get_product_by_slug(self,slug):
        """Method to get the product based on slug"""
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            product = None
        except:
            print('500')
            raise Exception 
        return product
    
    