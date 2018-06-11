import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django import db
from django.views import View
from django.shortcuts import render, redirect, HttpResponse
from django.utils.http import is_safe_url

from ..carts.backend.backend import CartBackend

from .models import Account, AccountAddress

class AccountBaseClass(View):
    def __init__(self):
        self.account_obj = Account.objects

        
class LoginView(AccountBaseClass):
    
    """Login page View"""
    
    def get(self,request):
        """Replace the code, added to test"""
        try:
            return render(request,'login.html',{})
        except:
            pass
        
    def post(self,request):
        
        """
        Authenticate and log in a user and redirect him to the home page.
        If not authenticated reload the pgae with error in the context dict
        """
    
        try:
            username     = request.POST['email']
            password     = request.POST['password']
            next_        = request.GET.get('next')
            next_post    = request.POST.get('next')
            next_url     = next_ or next_post
            user = authenticate(request, username=username, password=password)
            if user is not None:
                CartBackend().updateCartWithUser(user, request.session.get('cart_id'))
                login(request, user)
                """Also set the userid and account id in session so that we dont have to make db
                calls for these details"""
                if is_safe_url(next_url, request.get_host()):
                    redirect(next_url)
                else:
                    return redirect("/")
            else:
                return render(request,'login.html',{'invalid_user':True})
        except:
            print('500') 

class RegisterView(AccountBaseClass):
    """
    View to Register a User
    """
    
    def post(self,request):
        """
        Create an User
        """
        first_name  = request.POST.get('first_name')
        last_name   = request.POST.get('last_name')
        password    = request.POST.get('password')
        email       = request.POST.get('email_id')
        """
        can keep username as the emailid. Can think of some other logic
        or maybe can do an ajax call while entering username to check if it already exists.
        Also can create user based on either email or mobile
        """
        try:
            user = User.objects.create_user(email, email, password)
            if user:
                """
                Login him and redirect to the login Page. Send account Activation Mailer??
                Also set the userid and account id in session so that we dont have to make db
                calls for these details
                """
                login(request, user)
                self.account_obj.create_account(user ,first_name, last_name, email)
                return redirect('/')
        except db.IntegrityError:
            return render(request,'login.html',{'user_exists':True})
        except Exception as ex:
            print("500::"+ex.message)   
            

class UpdateAddress(AccountBaseClass):
    
    """
        View to update the address for an account
    """
    
    def post(self,request):
        try:
            address_obj     = AccountAddress.objects
            address_details = request.POST
            address_obj.update_address(request.user,address_details)
            response = {'response':True} 
        except:
            response = {'response':False}
        return HttpResponse(json.dumps(response), content_type="application/json")
            