from django.contrib import admin
from ..carts.models import CartDetails, Cart

# Register your models here.

admin.site.register(Cart)
admin.site.register(CartDetails)