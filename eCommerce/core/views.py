from django.views import View
from django.shortcuts import render

from eCommerce.products.models import Product


class BaseView(View):
    pass

class HomePage(BaseView):
    
    """Home Page View"""
    def __init__(self):
        self.context = {}
        self.productdao_obj = Product.objects
        
    def get(self,request):
        """
        Write code to set a visit cookie id,
        Also while getting featured items get only first 10-12
        counts based on what can be accomodated in home page.
        """
        featured_products = self.productdao_obj.get_products_by_feature(True)
        print(featured_products)
        self.context['featured_products'] = featured_products
        return render(request,'index.html',self.context)
    

