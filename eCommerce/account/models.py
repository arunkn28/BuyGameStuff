from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from .utils import ADDRESS_TYPE


class AccountManager(models.Manager):
    
    def create_account(self,user,first_name,last_name,email):
        return self.create(user=user,first_name=first_name, last_name=last_name, email=email)
    
    def get_account_by_id(self,account_id):
        return self.filter(id=id)
    
    def get_account_by_user(self,user_id):
        return self.filter(user=user_id)
    
class Account(models.Model):
    user                  = models.OneToOneField(User)
    first_name            = models.CharField(max_length=50,default='')
    last_name             = models.CharField(max_length=50,default='')
    email                 = models.EmailField(max_length=250)
    phone_regex           = RegexValidator(regex=r'^\+91[7-9]\d{9}$')
    phone_number          = models.CharField(validators=[phone_regex], max_length=17, null=True) 
    created_by            = models.CharField(max_length=50, default='account')
    created_datetime      = models.DateField(auto_now_add=True)
    modified_by           = models.CharField(max_length=50, default='')
    modified_datetime     = models.DateField(null=True,auto_now=True)
    
    objects               = AccountManager()
    def __str__(self):
        return self.user.username


class AccountAddressManager(models.Manager):
    pass

class AccountAddress(models.Model):
    """
    Will have one is to one relation with account for now.
    Whenever customer chnages the address we update with the new one
    """
    account               = models.OneToOneField(Account)
    name                  = models.CharField(max_length=150)
    phone_regex           = RegexValidator(regex=r'^\+91[7-9]\d{9}$')
    phone_number          = models.CharField(validators=[phone_regex], max_length=17, null=True) 
    building_info         = models.CharField(max_length=500,default='')
    area                  = models.CharField(max_length=500,default='')
    city                  = models.CharField(max_length=50,default='')
    pincode               = models.PositiveIntegerField()
    state                 = models.CharField(max_length=100,default='')
    address_type          = models.CharField(max_length=25,default='home',choices = ADDRESS_TYPE)
    objects               = AccountAddressManager()
    def __str__(self):
        return str(self.account.id)