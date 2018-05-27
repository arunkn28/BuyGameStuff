from django.shortcuts import render
from django.http.response import Http404
from django.views import View

from .models import Product, Category

# Create your views here.

class ProductBaseView(View):
        
    def __init__(self):
        self.context = {}
        self.product_obj = Product.objects
    
class ProductDetail(ProductBaseView):
    
    """View to show the detailed product description.
    Will get the slug being passed into this view,
    using which will filter the product and get the item details"""
    
    def get(self,request,slug=None):
        """
        DESC: Get the details of the product and populate it
        Chnanged the Product objects with the help of custom models managers in models.py
        Use slug instead of product id as we will be having product name in url slug
        which is better than having an id
        """
        try:
            product_details = self.product_obj.get_product_by_slug(slug)
            self.context['product_details'] = product_details
        except Product.DoesNotExist:
            raise Http404("No such product")
        except Exception:
            """render 500"""
            pass
        return render(request, 'product-details.html',self.context)

class ProductList(ProductBaseView):
    
    """List the complete products. 
    Check if the same view can be used to list all the Products
    for a given category, also use the same view for Search of a product
    Search can be based on query string and category wise losting will take it from
    regex slug"""
    
    """Use concept of Pagination"""
    def get(self,request, category_name=None):
        """Make a list of products and add it to the context"""
        try:
            if category_name: # Have to test this part and implememt preoperly
                category_id = Category.objects.filter(name=category_name).values('pk')[0].get('pk')
                all_products = self.product_obj.get(category_id=category_id)
            else:
                query = request.GET.get('q')
                all_products = self.product_obj.get_product_by_search(query)
                if not all_products:
                    raise Product.DoesNotExist
            self.context['all_products'] = all_products
            return render(request,'product-list.html',self.context)
        except Product.DoesNotExist:
            raise Http404('Hahaha nothing found')
        except:
            print('500')        
    