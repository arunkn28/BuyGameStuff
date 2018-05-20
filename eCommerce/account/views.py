from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.views import View
from django.shortcuts import render


class AccountBaseClass(View):
    pass

class LoginView(AccountBaseClass):
    
    """Login page View"""
    
    def get(self,request):
        """Replace the code added to test"""
        return render(request,'login.html',{})
    
    def post(self,request):
        
        """Authenticate and log in a user and redirect him to the home page.
        If not authenticated reload the pgae with error in the context dict"""
        
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            pass


class RegisterView(AccountBaseClass):
    """View to Register a User"""
    def get(self,request):
        pass
    
    def post(self,request):
        """Create an User"""
        #username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        """can keep username as the emailid. Can think of some other logic
        or maybe can do an ajax call while entering username to check if it already exists.
        Also can create user based on either email or mobile"""
        user = User.objects.create_user(email, email, password)
        if user:
            """Login him and redirect to the login Page"""
            
        else:
            """Throw error saying username or email already exists"""
            pass