from django.shortcuts import render
from django.views import View
# Create your views here.

class OrderViewBase(View):
    pass

class OrderView(OrderViewBase):
    
    def get(self,request):
        pass
    
    def post(self,request):
        pass
    
    
    