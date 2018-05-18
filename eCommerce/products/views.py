from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Product, Category
from django.http.response import HttpResponse
# Create your views here.

class ProductBaseView(View):
    pass

class ProductDetail(ProductBaseView):
    
    """View to show the detailed product description.
    Will get the product id being passed into this view,
    using which will filter the product and get the item details"""
    
    def get(self,request,product_id=None):
        product = get_object_or_404(Product, pk=product_id)
        
        """"Get the details of the product and populate it"""
        return HttpResponse("hiii"+str(product.product_title))


class ProductList(ProductBaseView):
    
    """List the complete products. 
    Check if the same view can be used to list all the Products
    for a given category, also use the same view for Search of a product
    Search can be based on query string and category wise losting will take it from
    regex slug"""
    
    def get(self,request, category_name=None):
        """Make a list of products and add it to the context"""
        try:
            category_id = Category.objects.filter(category_name=category_name).values('pk')[0].get('pk')
            all_products = Product.objects.get(category_id=category_id)
        except Product.DoesNotExist:
            print('Hahaha nothing found')
        except:
            print('500')        
        name = ''
        for product in all_products:
            name = name + product.product_title
        return HttpResponse("hiii"+str(name))
    