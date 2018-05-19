from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponse
from django.views import View

from .models import Product, Category
from .prodcuctDAO import ProductDAO

# Create your views here.

class ProductBaseView(View):
        
    def __init__(self):
        self.context = {}
    
class ProductDetail(ProductBaseView):
    
    """View to show the detailed product description.
    Will get the product id being passed into this view,
    using which will filter the product and get the item details"""
    
    def get(self,request,slug=None):
        """"Get the details of the product and populate it
        Chnanged the Product objects with the help of custom models managers in models.py
        Use slug instead of product id as we will be having product name in url slug
        which is better than having an id"""
        productdao = ProductDAO()
        product_details = productdao.get_product_by_slug(slug)
        self.context['product_details'] = product_details
        return render(request, 'product-details.html',self.context)

class ProductList(ProductBaseView):
    
    """List the complete products. 
    Check if the same view can be used to list all the Products
    for a given category, also use the same view for Search of a product
    Search can be based on query string and category wise losting will take it from
    regex slug"""
    
    def get(self,request, category_name=None):
        """Make a list of products and add it to the context"""
        try:
            category_id = Category.objects.filter(name=category_name).values('pk')[0].get('pk')
            all_products = Product.objects.get(category_id=category_id)
        except Product.DoesNotExist:
            print('Hahaha nothing found')
        except:
            print('500')        
        name = ''
        for product in all_products:
            name = name + product.name
        return HttpResponse("hiii"+str(name))
    