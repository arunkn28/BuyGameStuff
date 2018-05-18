from django.shortcuts import render
from djano.views import View
# Create your views here.

class ProductBaseView(View):
    pass

class ProductDetails(ProductBaseView):
    """View to show the detailed product description."""
    def get(self,request):
        pass
    


class ProductList(ProductBaseView):
    """List the complete products. 
    Check if the same view can be used to list all the Products
    for a given category, also use the same view for Search of a product"""
    def get(self,request):
        pass
    