from django.http import HttpResponse
from django.views import View

class BaseView(View):
    pass

class HomePage(BaseView):
    
    """Home Page View"""
    
    def get(self,request):
        return HttpResponse('<h1>Hello!!</h1>')
    

