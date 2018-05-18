from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

class BaseView(View):
    pass

class HomePage(BaseView):
    
    """Home Page View"""
    
    def get(self,request):
        return render(request,'index.html',{})
    

