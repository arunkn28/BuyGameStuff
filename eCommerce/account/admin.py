from django.contrib import admin

from .models import Account,AccountAddress
# Register your models here.

admin.site.register(Account)
admin.site.register(AccountAddress)