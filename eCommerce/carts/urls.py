from django.conf.urls import url

from .views import Carts

urlpatterns = [
    url(r'^$', Carts.as_view(),name='cart'),
    #url(r'^cart/$', ProductDetail.as_view(),name='productdetails'),
]