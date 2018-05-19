from django.views import View
from django.shortcuts import render

from eCommerce.products.prodcuctDAO import ProductDAO

class BaseView(View):
    pass

class HomePage(BaseView):
    
    """Home Page View"""
    def __init__(self):
        self.context = {}
        
    def get(self,request):
        """Write code to set a visit cookie id"""
        productdao = ProductDAO()
        featured_products = productdao.get_products_by_feature(True)
        print(featured_products)
        self.context['featured_products'] = featured_products
        return render(request,'index.html',self.context)
    

