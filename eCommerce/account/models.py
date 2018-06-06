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
    
    def seacrh_address_by_account(self,account_id):
        return self.filter(account_id=account_id)
    
    def update_address(self,user_id,address_details):
        account         = Account().get_account_by_user(user_id)
        account_address = self.seacrh_address_by_account(account.first().account_id)
        if account_address:
            self.update(first_name=address_details.get('first_name'),last_name=address_details.get('last_name'),
                        phone_number=address_details.get('phone_number'),
                        building_info=address_details.get('building_info'),area=address_details.get('area'),
                        city=address_details.get('city'),pincode=address_details.get('pincode'),
                        state=address_details.get('state'),address_type=address_details.get('address_type'))
        else:
            self.create(account=account.first(),first_name=address_details.get('first_name'),last_name=address_details.get('last_name'),
                        phone_number=address_details.get('phone_number'),
                        building_info=address_details.get('building_info'),area=address_details.get('area'),
                        city=address_details.get('city'),pincode=address_details.get('pincode'),
                        state=address_details.get('state'),address_type=address_details.get('address_type'))
            

class AccountAddress(models.Model):
    """
    Will have one is to one relation with account for now.
    Whenever customer chnages the address we update with the new one
    """
    account               = models.OneToOneField(Account)
    first_name            = models.CharField(max_length=50)
    last_name             = models.CharField(max_length=50)
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