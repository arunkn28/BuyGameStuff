from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import RegexValidator


class AccountManager(models.Manager):
    
    def create_account(self,user_id,first_name,last_name,email):
        return self.create(user_id=user_id,first_name=first_name, last_name=last_name, email=email)
    
    def get_account_by_id(self,account_id):
        return self.filter(id=id)
    
    def get_account_by_user(self,user_id):
        return self.filter(user=user_id)
    
class Account(models.Model):
    user                  = models.ForeignKey(User)
    first_name            = models.CharField(max_length=50,default='')
    last_name             = models.CharField(max_length=50,default='')
    email                 = models.EmailField(max_length=250)
    phone_regex           = RegexValidator(regex=r'^\+91[7-9]\d{9}$')
    phone_number          = models.CharField(validators=[phone_regex], max_length=17, null=True) 
    created_by            = models.CharField(max_length=50, default='account')
    created_datetime      = models.DateField(auto_now=True)
    modified_by           = models.CharField(max_length=50, default='')
    modified_datetime     = models.DateField(null=True)
    
    objects               = AccountManager()
    def __str__(self):
        return self.user.username
